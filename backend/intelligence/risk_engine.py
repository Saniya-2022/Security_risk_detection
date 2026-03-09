"""
Advanced Risk Scoring Engine
Calculates comprehensive risk scores based on multiple factors
"""
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class RiskEngine:
    def __init__(self):
        self.severity_weights = {
            'HIGH': 100,
            'MEDIUM': 60,
            'LOW': 30,
            'INFO': 10
        }
        
        self.threat_type_weights = {
            'ransomware': 1.5,
            'exploit': 1.4,
            'backdoor': 1.4,
            'malware': 1.3,
            'brute_force': 1.2,
            'phishing': 1.2,
            'dos': 1.1,
            'probe': 0.8,
            'analysis': 0.7
        }
    
    def calculate_risk_score(
        self,
        ml_confidence: float = 0.0,
        severity: str = 'LOW',
        frequency_score: float = 0.0,
        threat_intel_score: int = 0,
        anomaly_score: float = 0.0,
        threat_type: str = None
    ) -> Dict:
        """
        Calculate comprehensive risk score (0-100)
        
        Formula:
        Risk = (ML Confidence * 0.5) + 
               (Severity Weight * 0.2) + 
               (Frequency Score * 0.1) + 
               (Threat Intelligence Score * 0.1) + 
               (Anomaly Score * 0.1)
        """
        
        # ML Confidence component (0-50 points)
        ml_component = ml_confidence * 50
        
        # Severity component (0-20 points)
        severity_weight = self.severity_weights.get(severity.upper(), 30)
        severity_component = (severity_weight / 100) * 20
        
        # Frequency component (0-10 points)
        frequency_component = min(frequency_score, 1.0) * 10
        
        # Threat Intelligence component (0-10 points)
        threat_intel_component = (threat_intel_score / 100) * 10
        
        # Anomaly component (0-10 points)
        anomaly_component = min(anomaly_score, 1.0) * 10
        
        # Base risk score
        base_risk = (
            ml_component +
            severity_component +
            frequency_component +
            threat_intel_component +
            anomaly_component
        )
        
        # Apply threat type multiplier
        threat_multiplier = 1.0
        if threat_type:
            threat_lower = threat_type.lower()
            for key, multiplier in self.threat_type_weights.items():
                if key in threat_lower:
                    threat_multiplier = multiplier
                    break
        
        final_risk = min(base_risk * threat_multiplier, 100)
        
        # Determine risk level
        if final_risk >= 75:
            risk_level = 'CRITICAL'
        elif final_risk >= 60:
            risk_level = 'HIGH'
        elif final_risk >= 40:
            risk_level = 'MEDIUM'
        elif final_risk >= 20:
            risk_level = 'LOW'
        else:
            risk_level = 'INFO'
        
        result = {
            'risk_score': round(final_risk, 2),
            'risk_level': risk_level,
            'components': {
                'ml_confidence': round(ml_component, 2),
                'severity': round(severity_component, 2),
                'frequency': round(frequency_component, 2),
                'threat_intelligence': round(threat_intel_component, 2),
                'anomaly': round(anomaly_component, 2)
            },
            'threat_multiplier': threat_multiplier,
            'should_escalate': final_risk >= 75,
            'should_alert': final_risk >= 60,
            'should_create_incident': final_risk >= 75
        }
        
        logger.info(f"Risk calculated: {final_risk:.2f} ({risk_level})")
        return result
    
    def calculate_frequency_score(self, event_count: int, time_window_minutes: int) -> float:
        """
        Calculate frequency score based on event count in time window
        Returns 0.0 to 1.0
        """
        # Normalize: 10+ events in 5 minutes = 1.0
        normalized = (event_count / 10) * (5 / max(time_window_minutes, 1))
        return min(normalized, 1.0)
    
    def should_auto_escalate(self, risk_score: float, severity: str) -> bool:
        """Determine if alert should be auto-escalated"""
        if risk_score >= 75:
            return True
        if risk_score >= 60 and severity == 'MEDIUM':
            return True
        return False
    
    def get_recommended_actions(self, risk_score: float, threat_type: str = None) -> list:
        """Get recommended actions based on risk score"""
        actions = []
        
        if risk_score >= 75:
            actions.extend([
                'Create incident immediately',
                'Send email alert to SOC team',
                'Consider blocking source IP',
                'Escalate to senior analyst',
                'Enable enhanced monitoring'
            ])
        elif risk_score >= 60:
            actions.extend([
                'Review alert details',
                'Check for related events',
                'Monitor source IP',
                'Document findings'
            ])
        elif risk_score >= 40:
            actions.extend([
                'Log for future reference',
                'Check if part of larger pattern'
            ])
        else:
            actions.append('Monitor passively')
        
        # Threat-specific actions
        if threat_type:
            threat_lower = threat_type.lower()
            if 'brute_force' in threat_lower:
                actions.append('Consider account lockout policy')
            elif 'phishing' in threat_lower:
                actions.append('Warn affected users')
            elif 'malware' in threat_lower:
                actions.append('Isolate affected system')
            elif 'dos' in threat_lower:
                actions.append('Enable rate limiting')
        
        return actions


# Global instance
risk_engine = RiskEngine()
