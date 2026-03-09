"""
Event Correlation Engine
Correlates multiple events into incidents and detects attack patterns
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import logging
import uuid

logger = logging.getLogger(__name__)

class CorrelationEngine:
    def __init__(self, db):
        self.db = db
        self.alert_buffer = defaultdict(list)  # Temporary buffer for correlation
        self.correlation_rules = self._initialize_rules()
        
    def _initialize_rules(self) -> List[Dict]:
        """Initialize correlation rules"""
        return [
            {
                'rule_id': 'brute_force_pattern',
                'name': 'Brute Force Attack Pattern',
                'description': '5+ failed logins followed by success within 5 minutes',
                'conditions': {
                    'event_types': ['login', 'authentication'],
                    'time_window': 300,  # 5 minutes
                    'min_events': 5,
                    'pattern': 'failed_then_success'
                },
                'severity': 'HIGH',
                'mitre_tactic': 'Credential Access',
                'mitre_technique': 'T1110'
            },
            {
                'rule_id': 'escalation_pattern',
                'name': 'Alert Escalation Pattern',
                'description': 'Same IP triggers 3+ MEDIUM alerts within 10 minutes',
                'conditions': {
                    'severity': 'MEDIUM',
                    'time_window': 600,  # 10 minutes
                    'min_events': 3,
                    'group_by': 'source_ip'
                },
                'severity': 'HIGH',
                'mitre_tactic': 'Persistence',
                'mitre_technique': 'T1078'
            },
            {
                'rule_id': 'suspicious_access_pattern',
                'name': 'Suspicious Access Pattern',
                'description': 'Same user accessed from 2+ different countries within 30 minutes',
                'conditions': {
                    'time_window': 1800,  # 30 minutes
                    'min_events': 2,
                    'group_by': 'target_user',
                    'different_countries': True
                },
                'severity': 'HIGH',
                'mitre_tactic': 'Initial Access',
                'mitre_technique': 'T1078'
            },
            {
                'rule_id': 'multi_stage_attack',
                'name': 'Multi-Stage Attack',
                'description': 'Probe followed by exploit within 15 minutes',
                'conditions': {
                    'event_sequence': ['probe', 'exploit'],
                    'time_window': 900,  # 15 minutes
                    'group_by': 'source_ip'
                },
                'severity': 'CRITICAL',
                'mitre_tactic': 'Initial Access',
                'mitre_technique': 'T1190'
            },
            {
                'rule_id': 'repeated_high_alerts',
                'name': 'Repeated High Severity Alerts',
                'description': '3+ HIGH alerts from same source within 5 minutes',
                'conditions': {
                    'severity': 'HIGH',
                    'time_window': 300,
                    'min_events': 3,
                    'group_by': 'source_ip'
                },
                'severity': 'CRITICAL',
                'mitre_tactic': 'Impact',
                'mitre_technique': 'T1499'
            }
        ]
    
    async def correlate_alert(self, alert: Dict) -> Optional[Dict]:
        """
        Correlate new alert with existing alerts
        Returns incident if correlation rule matches
        """
        source_ip = alert.get('source_ip')
        target_user = alert.get('target_user')
        severity = alert.get('severity')
        threat_type = alert.get('threat_type', '')
        
        # Add to buffer
        buffer_key = source_ip or target_user or 'unknown'
        self.alert_buffer[buffer_key].append({
            'alert': alert,
            'timestamp': datetime.utcnow()
        })
        
        # Clean old entries from buffer (older than 30 minutes)
        self._clean_buffer()
        
        # Check each correlation rule
        for rule in self.correlation_rules:
            incident = await self._check_rule(rule, alert, buffer_key)
            if incident:
                logger.info(f"Correlation rule triggered: {rule['name']}")
                return incident
        
        return None
    
    async def _check_rule(self, rule: Dict, current_alert: Dict, buffer_key: str) -> Optional[Dict]:
        """Check if correlation rule matches"""
        conditions = rule['conditions']
        time_window = conditions.get('time_window', 300)
        min_events = conditions.get('min_events', 2)
        
        # Get recent alerts from buffer
        now = datetime.utcnow()
        recent_alerts = [
            item for item in self.alert_buffer[buffer_key]
            if (now - item['timestamp']).total_seconds() <= time_window
        ]
        
        if len(recent_alerts) < min_events:
            return None
        
        # Check specific rule conditions
        rule_id = rule['rule_id']
        
        if rule_id == 'brute_force_pattern':
            return await self._check_brute_force(rule, recent_alerts, current_alert)
        
        elif rule_id == 'escalation_pattern':
            return await self._check_escalation(rule, recent_alerts, current_alert)
        
        elif rule_id == 'suspicious_access_pattern':
            return await self._check_suspicious_access(rule, recent_alerts, current_alert)
        
        elif rule_id == 'multi_stage_attack':
            return await self._check_multi_stage(rule, recent_alerts, current_alert)
        
        elif rule_id == 'repeated_high_alerts':
            return await self._check_repeated_high(rule, recent_alerts, current_alert)
        
        return None
    
    async def _check_brute_force(self, rule: Dict, recent_alerts: List, current_alert: Dict) -> Optional[Dict]:
        """Check brute force pattern"""
        # Count failed logins
        failed_count = sum(
            1 for item in recent_alerts
            if 'failed' in item['alert'].get('threat_type', '').lower() or
               'brute' in item['alert'].get('threat_type', '').lower()
        )
        
        # Check if current is success after failures
        current_threat = current_alert.get('threat_type', '').lower()
        if failed_count >= 4 and 'normal' in current_threat:
            return await self._create_incident(
                rule=rule,
                alerts=recent_alerts + [{'alert': current_alert, 'timestamp': datetime.utcnow()}],
                title=f"Brute Force Attack Detected - {current_alert.get('source_ip')}",
                description=f"Detected {failed_count} failed login attempts followed by successful login"
            )
        
        return None
    
    async def _check_escalation(self, rule: Dict, recent_alerts: List, current_alert: Dict) -> Optional[Dict]:
        """Check alert escalation pattern"""
        medium_alerts = [
            item for item in recent_alerts
            if item['alert'].get('severity') == 'MEDIUM'
        ]
        
        if len(medium_alerts) >= 3:
            return await self._create_incident(
                rule=rule,
                alerts=medium_alerts,
                title=f"Alert Escalation - {current_alert.get('source_ip')}",
                description=f"Multiple MEDIUM alerts ({len(medium_alerts)}) from same source - escalating to HIGH"
            )
        
        return None
    
    async def _check_suspicious_access(self, rule: Dict, recent_alerts: List, current_alert: Dict) -> Optional[Dict]:
        """Check suspicious access from different locations"""
        countries = set()
        for item in recent_alerts:
            enrichment = item['alert'].get('threat_intelligence', {})
            country = enrichment.get('country')
            if country:
                countries.add(country)
        
        if len(countries) >= 2:
            return await self._create_incident(
                rule=rule,
                alerts=recent_alerts,
                title=f"Suspicious Access Pattern - {current_alert.get('target_user')}",
                description=f"User accessed from {len(countries)} different countries: {', '.join(countries)}"
            )
        
        return None
    
    async def _check_multi_stage(self, rule: Dict, recent_alerts: List, current_alert: Dict) -> Optional[Dict]:
        """Check multi-stage attack pattern"""
        threat_types = [item['alert'].get('threat_type', '').lower() for item in recent_alerts]
        
        # Check for probe followed by exploit
        has_probe = any('probe' in t or 'recon' in t for t in threat_types)
        has_exploit = any('exploit' in t or 'attack' in t for t in threat_types)
        
        if has_probe and has_exploit:
            return await self._create_incident(
                rule=rule,
                alerts=recent_alerts,
                title=f"Multi-Stage Attack Detected - {current_alert.get('source_ip')}",
                description="Detected reconnaissance followed by exploitation attempt"
            )
        
        return None
    
    async def _check_repeated_high(self, rule: Dict, recent_alerts: List, current_alert: Dict) -> Optional[Dict]:
        """Check repeated high severity alerts"""
        high_alerts = [
            item for item in recent_alerts
            if item['alert'].get('severity') == 'HIGH'
        ]
        
        if len(high_alerts) >= 3:
            return await self._create_incident(
                rule=rule,
                alerts=high_alerts,
                title=f"Critical: Repeated High Severity Alerts - {current_alert.get('source_ip')}",
                description=f"Detected {len(high_alerts)} HIGH severity alerts in short time window"
            )
        
        return None
    
    async def _create_incident(self, rule: Dict, alerts: List, title: str, description: str) -> Dict:
        """Create incident from correlated alerts"""
        incident_id = str(uuid.uuid4())
        alert_ids = [item['alert'].get('_id') for item in alerts if item['alert'].get('_id')]
        
        incident = {
            'incident_id': incident_id,
            'title': title,
            'description': description,
            'severity': rule['severity'],
            'status': 'Open',
            'related_alert_ids': alert_ids,
            'alert_count': len(alerts),
            'correlation_rule': rule['rule_id'],
            'mitre_tactic': rule.get('mitre_tactic'),
            'mitre_technique': rule.get('mitre_technique'),
            'assigned_analyst': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'timeline': [
                {
                    'timestamp': datetime.utcnow(),
                    'action': 'incident_created',
                    'description': f"Incident created by correlation rule: {rule['name']}"
                }
            ],
            'notes': []
        }
        
        # Save to database
        try:
            result = await self.db.incidents.insert_one(incident)
            incident['_id'] = result.inserted_id
            
            # Update related alerts with incident_id
            if alert_ids:
                await self.db.alerts.update_many(
                    {'_id': {'$in': alert_ids}},
                    {'$set': {'incident_id': incident_id}}
                )
            
            logger.info(f"Created incident: {incident_id} - {title}")
            return incident
            
        except Exception as e:
            logger.error(f"Error creating incident: {e}")
            return None
    
    def _clean_buffer(self):
        """Remove old entries from buffer"""
        now = datetime.utcnow()
        cutoff = timedelta(minutes=30)
        
        for key in list(self.alert_buffer.keys()):
            self.alert_buffer[key] = [
                item for item in self.alert_buffer[key]
                if now - item['timestamp'] < cutoff
            ]
            
            # Remove empty buffers
            if not self.alert_buffer[key]:
                del self.alert_buffer[key]
    
    async def deduplicate_alert(self, alert: Dict) -> bool:
        """
        Check if alert is duplicate
        Returns True if duplicate (should be ignored)
        """
        # Check for similar alert in last 5 minutes
        five_min_ago = datetime.utcnow() - timedelta(minutes=5)
        
        similar = await self.db.alerts.find_one({
            'source_ip': alert.get('source_ip'),
            'threat_type': alert.get('threat_type'),
            'target_user': alert.get('target_user'),
            'timestamp': {'$gte': five_min_ago}
        })
        
        return similar is not None
