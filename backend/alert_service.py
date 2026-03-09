"""
Alert Service - Processes events and creates alerts
"""

from datetime import datetime
from typing import Dict, Any
import logging

from backend.ml.ml_service import (
    predict_phishing_ml,
    predict_login_anomaly,
    predict_network_traffic,
    predict_malware
)
from backend.risk_engine import (
    calculate_dynamic_risk,
    generate_human_readable_alert,
    classify_severity
)
from backend.database.mongo import alerts_collection
from backend.security.ip_blocker import record_ip_violation, is_ip_blocked
from backend.runtime.email_service import send_alert_email
from backend.api.websocket_manager import manager

logger = logging.getLogger(__name__)


def serialize_datetime(obj):
    """Convert datetime objects to ISO format strings"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime(item) for item in obj]
    return obj


class AlertService:
    """Processes security events and generates alerts"""
    
    def __init__(self):
        self.email_recipient = "sreeja.warangal834@gmail.com"
    
    async def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process a security event and generate alert"""
        
        event_type = event.get("event_type")
        
        try:
            if event_type == "login":
                return await self._process_login_event(event)
            elif event_type == "network":
                return await self._process_network_event(event)
            elif event_type == "email":
                return await self._process_email_event(event)
            elif event_type == "malware":
                return await self._process_malware_event(event)
            else:
                logger.warning(f"Unknown event type: {event_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing event: {e}")
            return None
    
    async def _process_login_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process login event"""
        
        ip_address = event.get("ip_address")
        
        # Check if IP is blocked
        if is_ip_blocked(ip_address):
            logger.info(f"🚫 Blocked IP {ip_address} attempted login")
            return None
        
        # ML Prediction
        ml_result = predict_login_anomaly(event)
        
        # Calculate risk
        detection_data = {
            "failed_attempts": event.get("failed_attempts", 0),
            "ml_probability": ml_result["probability"]
        }
        risk_result = calculate_dynamic_risk(detection_data)
        
        # Determine threat type
        threat_type = "brute_force" if ml_result["is_anomaly"] else "normal_login"
        
        # Generate alert
        human_alert = generate_human_readable_alert(
            threat_type="brute_force" if ml_result["is_anomaly"] else "normal",
            risk_score=risk_result["risk_score"],
            severity=risk_result["severity"],
            details={
                "ip_address": ip_address,
                "username": event.get("username"),
                "country": event.get("country")
            },
            risk_factors=risk_result["risk_factors"]
        )
        
        # Create alert document
        timestamp = event.get("timestamp", datetime.utcnow())
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()
        
        # Serialize event details to handle datetime objects
        serialized_event = serialize_datetime(event)
        
        alert_data = {
            "event_type": "Login Attempt",
            "threat_type": threat_type,
            "source_ip": ip_address,
            "target_user": event.get("username"),
            "country": event.get("country"),
            "risk_score": risk_result["risk_score"],
            "severity": risk_result["severity"],
            "ml_confidence": ml_result["probability"],
            "detected_by": "Random Forest",
            "detection_method": "ML + Rules",
            "is_threat": ml_result["is_anomaly"],
            "details": serialized_event,
            "risk_factors": risk_result["risk_factors"],
            "human_readable_alert": human_alert,
            "timestamp": timestamp
        }
        
        # Save and broadcast
        await self._save_and_broadcast_alert(alert_data)
        
        # Handle HIGH severity
        if risk_result["severity"] == "HIGH":
            # Record violation
            record_ip_violation(
                ip_address,
                threat_type,
                risk_result["risk_score"],
                event
            )
            
            # Send email
            await self._send_email_notification(alert_data)
        
        return alert_data
    
    async def _process_network_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process network traffic event"""
        
        ip_address = event.get("ip_address")
        
        # Check if IP is blocked
        if is_ip_blocked(ip_address):
            logger.info(f"🚫 Blocked IP {ip_address} attempted network activity")
            return None
        
        # ML Prediction
        ml_result = predict_network_traffic(event)
        
        # Calculate risk
        detection_data = {
            "request_count": event.get("request_count_per_min", 0),
            "ml_probability": ml_result["probability"]
        }
        risk_result = calculate_dynamic_risk(detection_data)
        
        # Map attack type
        threat_type_map = {
            "DoS": "dos",
            "Probe": "probe",
            "BruteForce": "brute_force",
            "Normal": "normal_traffic"
        }
        threat_type = threat_type_map.get(ml_result["attack_type"], "unknown")
        
        # Generate alert
        human_alert = generate_human_readable_alert(
            threat_type=threat_type,
            risk_score=risk_result["risk_score"],
            severity=risk_result["severity"],
            details={"ip_address": ip_address, "port": event.get("port_number")},
            risk_factors=risk_result["risk_factors"]
        )
        
        # Create alert document
        timestamp = event.get("timestamp", datetime.utcnow())
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()
        
        # Serialize event details to handle datetime objects
        serialized_event = serialize_datetime(event)
        
        alert_data = {
            "event_type": "Network Traffic",
            "threat_type": threat_type,
            "attack_classification": ml_result["attack_type"],
            "source_ip": ip_address,
            "port": event.get("port_number"),
            "protocol": event.get("protocol"),
            "risk_score": risk_result["risk_score"],
            "severity": risk_result["severity"],
            "ml_confidence": ml_result["probability"],
            "detected_by": "Random Forest",
            "detection_method": "ML Classification",
            "is_threat": ml_result["attack_type"] != "Normal",
            "details": serialized_event,
            "risk_factors": risk_result["risk_factors"],
            "human_readable_alert": human_alert,
            "timestamp": timestamp
        }
        
        # Save and broadcast
        await self._save_and_broadcast_alert(alert_data)
        
        # Handle HIGH severity
        if risk_result["severity"] == "HIGH":
            record_ip_violation(ip_address, threat_type, risk_result["risk_score"], event)
            await self._send_email_notification(alert_data)
        
        return alert_data
    
    async def _process_email_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process email event"""
        
        # ML Prediction
        ml_result = predict_phishing_ml(event)
        
        # Calculate risk
        detection_data = {
            "suspicious_keywords": event.get("suspicious_keywords", 0),
            "num_links": event.get("num_links", 0),
            "ml_probability": ml_result["probability"]
        }
        risk_result = calculate_dynamic_risk(detection_data)
        
        # Generate alert
        human_alert = generate_human_readable_alert(
            threat_type="phishing" if ml_result["is_phishing"] else "normal",
            risk_score=risk_result["risk_score"],
            severity=risk_result["severity"],
            details={"sender": event.get("sender"), "subject": event.get("subject")},
            risk_factors=risk_result["risk_factors"]
        )
        
        # Create alert document
        timestamp = event.get("timestamp", datetime.utcnow())
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()
        
        # Serialize event details to handle datetime objects
        serialized_event = serialize_datetime(event)
        
        alert_data = {
            "event_type": "Email",
            "threat_type": "phishing" if ml_result["is_phishing"] else "legitimate_email",
            "source_email": event.get("sender"),
            "subject": event.get("subject"),
            "risk_score": risk_result["risk_score"],
            "severity": risk_result["severity"],
            "ml_confidence": ml_result["probability"],
            "detected_by": "Logistic Regression",
            "detection_method": "TF-IDF + ML",
            "is_threat": ml_result["is_phishing"],
            "details": serialized_event,
            "risk_factors": risk_result["risk_factors"],
            "human_readable_alert": human_alert,
            "timestamp": timestamp
        }
        
        # Save and broadcast
        await self._save_and_broadcast_alert(alert_data)
        
        # Handle HIGH severity
        if risk_result["severity"] == "HIGH":
            await self._send_email_notification(alert_data)
        
        return alert_data
    
    async def _process_malware_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process malware scan event"""
        
        # ML Prediction
        ml_result = predict_malware(event)
        
        # Calculate risk
        detection_data = {
            "ml_probability": ml_result["probability"]
        }
        risk_result = calculate_dynamic_risk(detection_data)
        
        # Generate alert
        human_alert = generate_human_readable_alert(
            threat_type="malware" if ml_result["is_malware"] else "normal",
            risk_score=risk_result["risk_score"],
            severity=risk_result["severity"],
            details={"file_name": event.get("file_name")},
            risk_factors=risk_result["risk_factors"]
        )
        
        # Create alert document
        timestamp = event.get("timestamp", datetime.utcnow())
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()
        
        # Serialize event details to handle datetime objects
        serialized_event = serialize_datetime(event)
        
        alert_data = {
            "event_type": "File Scan",
            "threat_type": "malware" if ml_result["is_malware"] else "safe_file",
            "file_name": event.get("file_name"),
            "file_extension": event.get("extension"),
            "risk_score": risk_result["risk_score"],
            "severity": risk_result["severity"],
            "ml_confidence": ml_result["probability"],
            "detected_by": "Random Forest",
            "detection_method": "ML Classification",
            "is_threat": ml_result["is_malware"],
            "details": serialized_event,
            "risk_factors": risk_result["risk_factors"],
            "human_readable_alert": human_alert,
            "timestamp": timestamp
        }
        
        # Save and broadcast
        await self._save_and_broadcast_alert(alert_data)
        
        # Handle HIGH severity
        if risk_result["severity"] == "HIGH":
            await self._send_email_notification(alert_data)
        
        return alert_data
    
    async def _save_and_broadcast_alert(self, alert_data: Dict[str, Any]):
        """Save alert to database and broadcast via WebSocket"""
        
        try:
            # Save to MongoDB
            result = alerts_collection.insert_one(alert_data)
            alert_data["_id"] = str(result.inserted_id)
            
            # Broadcast to WebSocket clients
            await manager.broadcast_alert(alert_data)
            
            logger.info(f"🚨 Alert generated: {alert_data['threat_type']} - {alert_data['severity']}")
            
        except Exception as e:
            logger.error(f"Error saving/broadcasting alert: {e}")
    
    async def _send_email_notification(self, alert_data: Dict[str, Any]):
        """Send email notification for HIGH severity alerts"""
        
        try:
            email_body = f"""
🚨 HIGH SEVERITY SECURITY ALERT

Event Type: {alert_data.get('event_type', 'Unknown')}
Threat Type: {alert_data.get('threat_type', 'Unknown')}
Risk Score: {alert_data['risk_score']}/100
Severity: {alert_data['severity']}
ML Confidence: {alert_data.get('ml_confidence', 0):.2%}
Detected By: {alert_data.get('detected_by', 'Unknown')}

Source Information:
{self._format_source_info(alert_data)}

Threat Indicators:
{self._format_risk_factors(alert_data.get('risk_factors', []))}

Recommended Action:
{self._get_recommended_action(alert_data)}

Timestamp: {alert_data.get('timestamp', datetime.utcnow())}

---
This alert was generated automatically by Mini SIEM.
"""
            
            send_alert_email(
                receiver_email=self.email_recipient,
                subject=f"🚨 HIGH ALERT: {alert_data.get('threat_type', 'Security Threat')}",
                body=email_body
            )
            
            logger.info(f"📧 Email notification sent for alert {alert_data.get('_id')}")
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
    
    def _format_source_info(self, alert_data: Dict[str, Any]) -> str:
        """Format source information for email"""
        info = []
        if "source_ip" in alert_data:
            info.append(f"  Source IP: {alert_data['source_ip']}")
        if "target_user" in alert_data:
            info.append(f"  Target User: {alert_data['target_user']}")
        if "source_email" in alert_data:
            info.append(f"  Source Email: {alert_data['source_email']}")
        if "file_name" in alert_data:
            info.append(f"  File Name: {alert_data['file_name']}")
        return "\n".join(info) if info else "  N/A"
    
    def _format_risk_factors(self, risk_factors: list) -> str:
        """Format risk factors for email"""
        if not risk_factors:
            return "  None detected"
        return "\n".join([f"  • {factor}" for factor in risk_factors])
    
    def _get_recommended_action(self, alert_data: Dict[str, Any]) -> str:
        """Get recommended action based on threat type"""
        threat_type = alert_data.get('threat_type', '')
        
        if 'brute_force' in threat_type:
            return "  • Block source IP immediately\n  • Lock affected user account\n  • Enable MFA"
        elif 'dos' in threat_type:
            return "  • Activate DDoS mitigation\n  • Block attacking IP ranges\n  • Scale infrastructure"
        elif 'phishing' in threat_type:
            return "  • Do not click any links\n  • Report to security team\n  • Block sender domain"
        elif 'malware' in threat_type:
            return "  • Quarantine file immediately\n  • Run full system scan\n  • Isolate affected system"
        else:
            return "  • Review and monitor activity\n  • Escalate if pattern continues"


# Global alert service instance
alert_service = AlertService()
