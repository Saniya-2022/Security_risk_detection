"""
Enhanced Risk Engine for Mini SIEM
Dynamic risk scoring with ML integration and human-readable alerts
"""

from datetime import datetime
from typing import Dict, List, Any


# ============================================
# DYNAMIC RISK SCORING RULES
# ============================================

RISK_RULES = {
    # Login-based risks
    "failed_attempts_high": {"threshold": 5, "score": 40, "description": "Multiple failed login attempts detected"},
    "failed_attempts_critical": {"threshold": 10, "score": 60, "description": "Excessive failed login attempts - possible brute force"},
    "suspicious_country": {"score": 20, "description": "Login from suspicious country"},
    "unusual_time": {"score": 15, "description": "Login at unusual time"},
    
    # Network-based risks
    "high_request_rate": {"threshold": 100, "score": 50, "description": "Abnormally high request rate detected"},
    "dos_pattern": {"threshold": 500, "score": 80, "description": "Possible DoS attack pattern"},
    "port_scanning": {"score": 45, "description": "Port scanning activity detected"},
    "suspicious_port": {"score": 30, "description": "Connection to suspicious port"},
    
    # Email-based risks
    "phishing_keywords": {"threshold": 3, "score": 30, "description": "Multiple phishing keywords detected"},
    "suspicious_links": {"threshold": 3, "score": 35, "description": "Multiple suspicious links in email"},
    "malicious_attachment": {"score": 70, "description": "Potentially malicious attachment detected"},
    
    # ML-based risks
    "ml_high_confidence": {"threshold": 0.7, "score": 50, "description": "ML model high confidence threat detection"},
    "ml_critical_confidence": {"threshold": 0.9, "score": 70, "description": "ML model critical confidence threat detection"},
}


# ============================================
# RISK CALCULATION ENGINE
# ============================================

def calculate_dynamic_risk(detection_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate dynamic risk score based on multiple factors
    """
    
    risk_score = 0
    risk_factors = []
    
    # Login anomaly scoring
    if "failed_attempts" in detection_data:
        attempts = detection_data["failed_attempts"]
        if attempts >= RISK_RULES["failed_attempts_critical"]["threshold"]:
            risk_score += RISK_RULES["failed_attempts_critical"]["score"]
            risk_factors.append(RISK_RULES["failed_attempts_critical"]["description"])
        elif attempts >= RISK_RULES["failed_attempts_high"]["threshold"]:
            risk_score += RISK_RULES["failed_attempts_high"]["score"]
            risk_factors.append(RISK_RULES["failed_attempts_high"]["description"])
    
    # Network traffic scoring
    if "request_count" in detection_data:
        count = detection_data["request_count"]
        if count >= RISK_RULES["dos_pattern"]["threshold"]:
            risk_score += RISK_RULES["dos_pattern"]["score"]
            risk_factors.append(RISK_RULES["dos_pattern"]["description"])
        elif count >= RISK_RULES["high_request_rate"]["threshold"]:
            risk_score += RISK_RULES["high_request_rate"]["score"]
            risk_factors.append(RISK_RULES["high_request_rate"]["description"])
    
    # Email phishing scoring
    if "suspicious_keywords" in detection_data:
        if detection_data["suspicious_keywords"] >= RISK_RULES["phishing_keywords"]["threshold"]:
            risk_score += RISK_RULES["phishing_keywords"]["score"]
            risk_factors.append(RISK_RULES["phishing_keywords"]["description"])
    
    if "num_links" in detection_data:
        if detection_data["num_links"] >= RISK_RULES["suspicious_links"]["threshold"]:
            risk_score += RISK_RULES["suspicious_links"]["score"]
            risk_factors.append(RISK_RULES["suspicious_links"]["description"])
    
    # ML probability scoring
    if "ml_probability" in detection_data:
        prob = detection_data["ml_probability"]
        if prob >= RISK_RULES["ml_critical_confidence"]["threshold"]:
            risk_score += RISK_RULES["ml_critical_confidence"]["score"]
            risk_factors.append(RISK_RULES["ml_critical_confidence"]["description"])
        elif prob >= RISK_RULES["ml_high_confidence"]["threshold"]:
            risk_score += RISK_RULES["ml_high_confidence"]["score"]
            risk_factors.append(RISK_RULES["ml_high_confidence"]["description"])
    
    # Cap at 100
    risk_score = min(risk_score, 100)
    
    # Determine severity
    if risk_score >= 71:
        severity = "HIGH"
    elif risk_score >= 31:
        severity = "MEDIUM"
    else:
        severity = "LOW"
    
    return {
        "risk_score": risk_score,
        "severity": severity,
        "risk_factors": risk_factors
    }


# ============================================
# SEVERITY CLASSIFICATION
# ============================================

def classify_severity(risk_score: int) -> str:
    """Classify severity based on risk score"""
    
    if risk_score >= 71:
        return "HIGH"
    elif risk_score >= 31:
        return "MEDIUM"
    else:
        return "LOW"


# ============================================
# HUMAN-READABLE ALERT GENERATOR
# ============================================

def generate_human_readable_alert(
    threat_type: str,
    risk_score: int,
    severity: str,
    details: Dict[str, Any],
    risk_factors: List[str]
) -> str:
    """
    Generate human-readable alert message
    """
    
    # Threat-specific descriptions
    threat_descriptions = {
        "phishing": "Suspicious phishing email detected",
        "brute_force": "Multiple failed login attempts detected",
        "dos": "Possible DoS attack detected due to excessive requests",
        "probe": "Network scanning/probing activity detected",
        "malware": "Potentially malicious file detected",
        "normal": "Normal activity - no threat detected",
        "legitimate_email": "Legitimate email - no threat detected",
        "normal_login": "Normal login activity",
        "normal_traffic": "Normal network traffic",
        "safe_file": "Safe file - no malware detected"
    }
    
    description = threat_descriptions.get(threat_type, "Security event detected")
    
    # Build alert message
    if severity == "LOW" and risk_score == 0:
        # For safe/normal events
        alert_parts = [f"{severity} Risk: {description}"]
    else:
        # For threats
        alert_parts = [f"{severity} Risk: {description}"]
    
    # Add IP if available
    if "ip_address" in details:
        alert_parts.append(f"from IP {details['ip_address']}")
    
    # Add specific details
    if risk_factors:
        alert_parts.append(f"\n\nThreat Indicators:\n" + "\n".join([f"• {factor}" for factor in risk_factors]))
    
    # Add recommended action
    action = get_recommended_action(severity, threat_type)
    alert_parts.append(f"\n\nRecommended Action:\n{action}")
    
    return ". ".join(alert_parts[:2]) + "".join(alert_parts[2:])


# ============================================
# RECOMMENDED ACTIONS
# ============================================

def get_recommended_action(severity: str, threat_type: str) -> str:
    """Get recommended action based on severity and threat type"""
    
    # Safe/Normal activity recommendations
    safe_actions = {
        "legitimate_email": "• Email appears safe\n• No action required\n• Continue normal operations",
        "normal_login": "• Login successful\n• No suspicious activity detected\n• Continue monitoring",
        "normal_traffic": "• Network traffic within normal parameters\n• No action required",
        "safe_file": "• File scan complete - no threats found\n• Safe to use\n• No action required"
    }
    
    # Check if it's a safe activity
    if threat_type in safe_actions:
        return safe_actions[threat_type]
    
    actions = {
        "HIGH": {
            "phishing": "• Do not click any links or download attachments\n• Report to security team immediately\n• Block sender domain",
            "brute_force": "• Block source IP address immediately\n• Lock affected user account\n• Enable MFA if not already active",
            "dos": "• Activate DDoS mitigation\n• Block attacking IP ranges\n• Scale infrastructure if needed",
            "probe": "• Block scanning IP address\n• Review firewall rules\n• Monitor for follow-up attacks",
            "malware": "• Quarantine file immediately\n• Run full system scan\n• Isolate affected system"
        },
        "MEDIUM": {
            "phishing": "• Verify sender authenticity\n• Do not respond to email\n• Report if confirmed malicious",
            "brute_force": "• Monitor login attempts\n• Consider temporary account lock\n• Review access logs",
            "dos": "• Monitor traffic patterns\n• Prepare mitigation measures\n• Alert network team",
            "probe": "• Log activity for analysis\n• Monitor for escalation\n• Review security posture",
            "malware": "• Scan file with updated antivirus\n• Do not execute file\n• Submit for analysis"
        },
        "LOW": {
            "default": "• Log event for monitoring\n• No immediate action required\n• Continue normal operations"
        }
    }
    
    if severity == "LOW":
        return actions["LOW"]["default"]
    
    return actions.get(severity, {}).get(threat_type, "• Review and monitor activity\n• Escalate if pattern continues")


# ============================================
# LEGACY COMPATIBILITY
# ============================================

def calculate_final_risk(events):
    """Legacy function for backward compatibility"""
    
    if not events:
        return 0, "LOW"
    
    total_score = sum(event.get("score", 0) for event in events)
    total_score = min(total_score, 100)
    
    severity = classify_severity(total_score)
    
    return total_score, severity


def process_security_events(events):
    """Legacy function for backward compatibility"""
    
    total_score, severity = calculate_final_risk(events)
    
    risk_factors = [event.get("reason", "Unknown issue") for event in events]
    
    alert_message = {
        "timestamp": datetime.utcnow().isoformat(),
        "severity": severity,
        "total_score": total_score,
        "summary": f"{severity} security threat detected",
        "details": risk_factors,
        "recommended_action": get_recommended_action(severity, "default")
    }
    
    return {
        "events": events,
        "total_score": total_score,
        "severity": severity,
        "containment_required": severity == "HIGH",
        "alert": alert_message
    }
