"""
Enterprise Alert Processing Service
Integrates ML detection, threat enrichment, anomaly detection, 
risk scoring, correlation, and incident management
"""
import asyncio
from datetime import datetime
from typing import Dict, Optional
import logging

from backend.intelligence.threat_enrichment import threat_enrichment
from backend.intelligence.mitre_mapper import mitre_mapper
from backend.intelligence.risk_engine import risk_engine
from backend.intelligence.anomaly_detector import anomaly_detector
from backend.intelligence.correlation_engine import CorrelationEngine

logger = logging.getLogger(__name__)

class EnterpriseAlertService:
    def __init__(self, db, websocket_manager, email_service=None):
        self.db = db
        self.websocket_manager = websocket_manager
        self.email_service = email_service
        self.correlation_engine = CorrelationEngine(db)
        
    async def process_event(self, event: Dict) -> Dict:
        """
        Complete enterprise event processing pipeline:
        1. ML Detection (already done)
        2. Threat Intelligence Enrichment
        3. Anomaly Detection
        4. MITRE ATT&CK Mapping
        5. Advanced Risk Scoring
        6. Event Correlation
        7. Incident Creation
        8. Storage & Broadcasting
        """
        try:
            logger.info(f"Processing event: {event.get('event_type')}")
            
            # Step 1: Threat Intelligence Enrichment
            if event.get('source_ip'):
                enrichment = threat_enrichment.enrich_ip(event['source_ip'])
                event['threat_intelligence'] = enrichment
                threat_intel_score = threat_enrichment.calculate_threat_score(enrichment)
            else:
                threat_intel_score = 0
            
            # Step 2: Anomaly Detection
            anomaly_result = anomaly_detector.detect_anomaly(event)
            event['anomaly_detection'] = anomaly_result
            anomaly_score = anomaly_result.get('anomaly_score', 0.0)
            
            # Step 3: MITRE ATT&CK Mapping
            threat_type = event.get('threat_type', '')
            mitre_mapping = mitre_mapper.map_threat(threat_type)
            if mitre_mapping:
                event['mitre_attack'] = mitre_mapping
            
            # Step 4: Advanced Risk Scoring
            ml_confidence = event.get('ml_confidence', 0.0)
            severity = event.get('severity', 'LOW')
            
            # Calculate frequency score (simplified - could query DB for actual frequency)
            frequency_score = 0.3 if anomaly_result.get('is_anomaly') else 0.1
            
            risk_result = risk_engine.calculate_risk_score(
                ml_confidence=ml_confidence,
                severity=severity,
                frequency_score=frequency_score,
                threat_intel_score=threat_intel_score,
                anomaly_score=anomaly_score,
                threat_type=threat_type
            )
            
            event['risk_analysis'] = risk_result
            event['risk_score'] = risk_result['risk_score']
            event['risk_level'] = risk_result['risk_level']
            
            # Auto-escalate if needed
            if risk_result.get('should_escalate'):
                event['severity'] = 'HIGH'
                event['auto_escalated'] = True
                logger.warning(f"Alert auto-escalated to HIGH: {event.get('event_type')}")
            
            # Get recommended actions
            event['recommended_actions'] = risk_engine.get_recommended_actions(
                risk_result['risk_score'],
                threat_type
            )
            
            # Step 5: Check for duplicates
            is_duplicate = await self.correlation_engine.deduplicate_alert(event)
            if is_duplicate:
                logger.info("Duplicate alert detected - skipping")
                return None
            
            # Step 6: Save alert to database
            event['timestamp'] = datetime.utcnow()
            event['processed_at'] = datetime.utcnow()
            
            result = await self.db.alerts.insert_one(event)
            event['_id'] = str(result.inserted_id)
            
            # Step 7: Event Correlation & Incident Creation
            incident = await self.correlation_engine.correlate_alert(event)
            if incident:
                event['incident_id'] = incident['incident_id']
                event['incident_created'] = True
                
                # Broadcast incident
                await self.websocket_manager.broadcast({
                    'type': 'incident',
                    'data': self._serialize_incident(incident)
                })
                
                logger.warning(f"Incident created: {incident['incident_id']} - {incident['title']}")
            
            # Step 8: Broadcast alert via WebSocket
            await self.websocket_manager.broadcast({
                'type': 'alert',
                'data': self._serialize_alert(event)
            })
            
            # Step 9: Send email for high-risk alerts
            if risk_result.get('should_alert') and self.email_service:
                await self._send_alert_email(event)
            
            # Step 10: Auto-block IP if critical
            if risk_result['risk_score'] >= 80 and event.get('source_ip'):
                await self._auto_block_ip(event)
            
            logger.info(f"Alert processed successfully: Risk={risk_result['risk_score']:.2f}, Severity={event['severity']}")
            return event
            
        except Exception as e:
            logger.error(f"Error processing event: {e}", exc_info=True)
            return None
    
    def _serialize_alert(self, alert: Dict) -> Dict:
        """Serialize alert for JSON transmission"""
        serialized = alert.copy()
        
        # Convert datetime objects
        if isinstance(serialized.get('timestamp'), datetime):
            serialized['timestamp'] = serialized['timestamp'].isoformat()
        if isinstance(serialized.get('processed_at'), datetime):
            serialized['processed_at'] = serialized['processed_at'].isoformat()
        
        # Convert ObjectId
        if '_id' in serialized:
            serialized['_id'] = str(serialized['_id'])
        
        return serialized
    
    def _serialize_incident(self, incident: Dict) -> Dict:
        """Serialize incident for JSON transmission"""
        serialized = incident.copy()
        
        # Convert datetime objects
        if isinstance(serialized.get('created_at'), datetime):
            serialized['created_at'] = serialized['created_at'].isoformat()
        if isinstance(serialized.get('updated_at'), datetime):
            serialized['updated_at'] = serialized['updated_at'].isoformat()
        
        # Convert timeline timestamps
        if 'timeline' in serialized:
            for event in serialized['timeline']:
                if isinstance(event.get('timestamp'), datetime):
                    event['timestamp'] = event['timestamp'].isoformat()
        
        # Convert ObjectId
        if '_id' in serialized:
            serialized['_id'] = str(serialized['_id'])
        
        return serialized
    
    async def _send_alert_email(self, alert: Dict):
        """Send email notification for high-risk alert"""
        try:
            if not self.email_service:
                return
            
            subject = f"🚨 {alert['severity']} Security Alert - {alert.get('threat_type', 'Unknown')}"
            
            body = f"""
Security Alert Detected

Severity: {alert['severity']}
Risk Score: {alert.get('risk_score', 0):.2f}/100
Threat Type: {alert.get('threat_type', 'Unknown')}
Source IP: {alert.get('source_ip', 'N/A')}
Target User: {alert.get('target_user', 'N/A')}

Threat Intelligence:
- Country: {alert.get('threat_intelligence', {}).get('country', 'Unknown')}
- Reputation: {alert.get('threat_intelligence', {}).get('reputation_score', 'N/A')}
- Blacklisted: {alert.get('threat_intelligence', {}).get('is_blacklisted', False)}

MITRE ATT&CK:
- Tactic: {alert.get('mitre_attack', {}).get('tactic', 'N/A')}
- Technique: {alert.get('mitre_attack', {}).get('technique_id', 'N/A')} - {alert.get('mitre_attack', {}).get('technique_name', 'N/A')}

Anomaly Detection:
- Is Anomaly: {alert.get('anomaly_detection', {}).get('is_anomaly', False)}
- Anomaly Score: {alert.get('anomaly_detection', {}).get('anomaly_score', 0):.2f}
- Types: {', '.join(alert.get('anomaly_detection', {}).get('anomaly_type', []))}

Recommended Actions:
{chr(10).join('- ' + action for action in alert.get('recommended_actions', []))}

Timestamp: {alert.get('timestamp', datetime.utcnow()).isoformat()}

---
Mini SIEM Enterprise Edition
"""
            
            await self.email_service.send_alert_email(
                subject=subject,
                body=body,
                alert_data=alert
            )
            
            logger.info(f"Alert email sent for {alert.get('event_type')}")
            
        except Exception as e:
            logger.error(f"Error sending alert email: {e}")
    
    async def _auto_block_ip(self, alert: Dict):
        """Automatically block IP for critical threats"""
        try:
            source_ip = alert.get('source_ip')
            if not source_ip:
                return
            
            # Check if already blocked
            existing = await self.db.blocked_ips.find_one({'ip_address': source_ip})
            
            if existing:
                # Increment block count
                await self.db.blocked_ips.update_one(
                    {'ip_address': source_ip},
                    {
                        '$inc': {'block_count': 1},
                        '$set': {'last_blocked': datetime.utcnow()}
                    }
                )
            else:
                # Add to blocked list
                await self.db.blocked_ips.insert_one({
                    'ip_address': source_ip,
                    'reason': f"Auto-blocked: {alert.get('threat_type')} (Risk: {alert.get('risk_score'):.2f})",
                    'blocked_at': datetime.utcnow(),
                    'last_blocked': datetime.utcnow(),
                    'block_count': 1,
                    'severity': alert.get('severity'),
                    'auto_blocked': True
                })
            
            # Broadcast IP block event
            await self.websocket_manager.broadcast({
                'type': 'ip_blocked',
                'data': {
                    'ip_address': source_ip,
                    'reason': alert.get('threat_type'),
                    'risk_score': alert.get('risk_score')
                }
            })
            
            logger.warning(f"IP auto-blocked: {source_ip} (Risk: {alert.get('risk_score'):.2f})")
            
        except Exception as e:
            logger.error(f"Error auto-blocking IP: {e}")
