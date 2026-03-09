# 🧪 ENTERPRISE SIEM API TESTING GUIDE

## Quick Start

1. Start the backend:
```bash
START_ENTERPRISE_SIEM.bat
```

2. Open Swagger docs: http://localhost:8000/docs

---

## 📡 CORE ENDPOINTS

### System Status
```bash
# Get system status
curl http://localhost:8000/system/status

# Health check
curl http://localhost:8000/system/health

# Root info
curl http://localhost:8000/
```

**Expected Response**:
```json
{
  "status": "operational",
  "mode": "enterprise",
  "total_alerts": 150,
  "total_incidents": 5,
  "open_incidents": 2,
  "intelligence_modules": {
    "mitre_mapper": "active",
    "threat_enrichment": "active",
    "anomaly_detector": "active",
    "risk_engine": "active",
    "correlation_engine": "active"
  }
}
```

---

## 🚨 ALERT ENDPOINTS

### Get All Alerts
```bash
curl http://localhost:8000/alerts?limit=10
```

### Get Alert by Severity
```bash
curl http://localhost:8000/alerts/severity/HIGH
```

### Get Alert Statistics
```bash
curl http://localhost:8000/alerts/stats
```

**Expected Response**:
```json
{
  "total_alerts": 150,
  "by_severity": {
    "HIGH": 25,
    "MEDIUM": 60,
    "LOW": 65
  },
  "threat_distribution": [
    {"_id": "brute_force", "count": 30},
    {"_id": "phishing", "count": 25}
  ],
  "mitre_distribution": [
    {"_id": "Credential Access", "count": 30},
    {"_id": "Initial Access", "count": 25}
  ],
  "risk_distribution": [
    {"_id": "HIGH", "count": 40},
    {"_id": "MEDIUM", "count": 60}
  ]
}
```

---

## 📋 INCIDENT ENDPOINTS

### Get All Incidents
```bash
curl http://localhost:8000/incidents
```

### Get Incident by ID
```bash
curl http://localhost:8000/incidents/{incident_id}
```

### Filter Incidents by Status
```bash
curl "http://localhost:8000/incidents?status=Open"
```

### Update Incident Status
```bash
curl -X PATCH "http://localhost:8000/incidents/{incident_id}/status?status=Investigating"
```

### Assign Incident to Analyst
```bash
curl -X PATCH "http://localhost:8000/incidents/{incident_id}/assign?analyst=john.doe"
```

### Add Note to Incident
```bash
curl -X POST "http://localhost:8000/incidents/{incident_id}/notes" \
  -H "Content-Type: application/json" \
  -d '{
    "analyst": "john.doe",
    "content": "Investigating source IP. Appears to be compromised host."
  }'
```

### Get Incident Statistics
```bash
curl http://localhost:8000/incidents/stats/summary
```

**Expected Response**:
```json
{
  "total_incidents": 12,
  "recent_24h": 5,
  "by_status": {
    "Open": 3,
    "Investigating": 4,
    "Resolved": 5,
    "Closed": 0
  },
  "by_severity": {
    "CRITICAL": 2,
    "HIGH": 5,
    "MEDIUM": 3,
    "LOW": 2
  }
}
```

### Create Manual Incident
```bash
curl -X POST "http://localhost:8000/incidents" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Suspicious Activity from External IP",
    "description": "Multiple failed login attempts detected",
    "severity": "HIGH",
    "related_alert_ids": ["alert_id_1", "alert_id_2"],
    "source_ip": "192.168.1.100",
    "target_user": "admin"
  }'
```

---

## 🧠 INTELLIGENCE ENDPOINTS

### MITRE ATT&CK Tactics
```bash
curl http://localhost:8000/intelligence/mitre/tactics
```

**Expected Response**:
```json
{
  "tactics": [
    "Credential Access",
    "Defense Evasion",
    "Discovery",
    "Execution",
    "Exfiltration",
    "Impact",
    "Initial Access",
    "Lateral Movement",
    "Persistence",
    "Reconnaissance"
  ]
}
```

### MITRE Techniques by Tactic
```bash
curl http://localhost:8000/intelligence/mitre/techniques/Credential%20Access
```

**Expected Response**:
```json
{
  "tactic": "Credential Access",
  "techniques": [
    {
      "threat_type": "brute_force",
      "technique_id": "T1110",
      "technique_name": "Brute Force"
    }
  ]
}
```

### IP Threat Intelligence
```bash
curl http://localhost:8000/intelligence/ip/8.8.8.8
```

**Expected Response**:
```json
{
  "ip_address": "8.8.8.8",
  "country": "United States",
  "country_code": "US",
  "city": "Mountain View",
  "asn": "AS15169",
  "org": "Google LLC",
  "is_blacklisted": false,
  "is_high_risk_country": false,
  "is_malicious_asn": false,
  "reputation_score": 100,
  "threat_level": "clean"
}
```

### User Behavioral Profile
```bash
curl http://localhost:8000/intelligence/user/john.doe
```

**Expected Response**:
```json
{
  "user": "john.doe",
  "total_logins": 45,
  "unique_ips": 3,
  "last_seen": "2024-01-15T10:30:00",
  "typical_login_hours": [8, 9, 10, 14, 15, 16]
}
```

### Correlation Engine Stats
```bash
curl http://localhost:8000/intelligence/correlation/stats
```

**Expected Response**:
```json
{
  "total_keys": 25,
  "total_events": 150,
  "active_rules": 6
}
```

---

## 🔒 SECURITY ENDPOINTS

### Get Blocked IPs
```bash
curl http://localhost:8000/security/blocked-ips
```

### Block IP Address
```bash
curl -X POST "http://localhost:8000/security/block-ip?ip_address=192.168.1.100&reason=Manual%20block%20-%20suspicious%20activity"
```

### Unblock IP Address
```bash
curl -X POST "http://localhost:8000/security/unblock-ip?ip_address=192.168.1.100"
```

---

## 🎮 CONTROL ENDPOINTS

### Start Event Generation
```bash
curl -X POST http://localhost:8000/control/start-events
```

### Stop Event Generation
```bash
curl -X POST http://localhost:8000/control/stop-events
```

---

## 🔌 WEBSOCKET CONNECTION

### JavaScript Example
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('Connected to Enterprise SIEM');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  switch(message.type) {
    case 'alert':
      console.log('New Alert:', message.data);
      break;
    case 'incident':
      console.log('New Incident:', message.data);
      break;
    case 'statistics':
      console.log('Stats Update:', message.data);
      break;
    case 'ip_blocked':
      console.log('IP Blocked:', message.data);
      break;
  }
};
```

### Python Example
```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"Received: {data['type']}")
    
ws = websocket.WebSocketApp(
    "ws://localhost:8000/ws",
    on_message=on_message
)
ws.run_forever()
```

---

## 🧪 TESTING SCENARIOS

### Scenario 1: Brute Force Detection
1. Generate 5+ failed login events from same IP
2. Wait for correlation engine to detect pattern
3. Check `/incidents` for new "Brute Force Attack" incident
4. Verify IP is blocked after 2 HIGH violations

### Scenario 2: Suspicious Access
1. Generate login from user in Country A
2. Generate login from same user in Country B within 30 min
3. Check for "Suspicious Access - Impossible Travel" incident

### Scenario 3: Port Scan Detection
1. Generate 10+ probe events from same IP
2. Check for "Port Scan Detected" incident

### Scenario 4: Alert Escalation
1. Generate 3 MEDIUM alerts from same IP within 10 min
2. Check for "Alert Escalation" incident
3. Verify severity escalated to HIGH

---

## 📊 SAMPLE ALERT STRUCTURE

```json
{
  "_id": "alert_id_123",
  "timestamp": "2024-01-15T10:30:00Z",
  "event_type": "login_attempt",
  "threat_type": "brute_force",
  "severity": "HIGH",
  "source_ip": "192.168.1.100",
  "target_user": "admin",
  "ml_confidence": 0.92,
  "detection_method": "ML - Network Analyzer",
  "detected_by": "network_ml_model",
  "risk_score": 85,
  "risk_level": "CRITICAL",
  "needs_escalation": true,
  "threat_enrichment": {
    "country": "China",
    "country_code": "CN",
    "city": "Beijing",
    "asn": "AS4134",
    "is_blacklisted": false,
    "is_high_risk_country": true,
    "reputation_score": 70,
    "threat_level": "suspicious"
  },
  "anomaly_detection": {
    "has_anomaly": true,
    "anomaly_score": 0.8,
    "anomaly_types": ["login_time", "rare_ip"],
    "details": {
      "login_time": {
        "is_anomaly": true,
        "anomaly_score": 0.8,
        "reason": "Login at unusual hour (3:00, typical: 9:00)"
      }
    }
  },
  "mitre_attack": {
    "tactic": "Credential Access",
    "technique_id": "T1110",
    "technique_name": "Brute Force",
    "description": "Adversaries may use brute force techniques to gain access"
  },
  "risk_factors": [
    "Multiple failed login attempts",
    "High-risk country: China",
    "Anomaly: Login at unusual hour",
    "IP reputation: suspicious"
  ],
  "incident_id": "incident_456"
}
```

---

## 📊 SAMPLE INCIDENT STRUCTURE

```json
{
  "incident_id": "incident_456",
  "title": "Brute Force Attack Detected",
  "description": "5 failed login attempts followed by successful login",
  "severity": "HIGH",
  "status": "Open",
  "related_alert_ids": ["alert_1", "alert_2", "alert_3"],
  "related_alert_count": 3,
  "correlation_rule": "brute_force_attack",
  "source_ip": "192.168.1.100",
  "target_user": "admin",
  "mitre_tactic": "Credential Access",
  "mitre_technique": "T1110",
  "mitre_technique_name": "Brute Force",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "assigned_analyst": null,
  "timeline": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "action": "Incident Created",
      "details": "Automatically created by correlation rule: brute_force_attack"
    }
  ],
  "notes": []
}
```

---

## 🎯 SUCCESS INDICATORS

✅ **System is working correctly if you see**:
- Alerts with `threat_enrichment` field (GeoIP data)
- Alerts with `anomaly_detection` field (behavioral analysis)
- Alerts with `mitre_attack` field (MITRE mapping)
- Alerts with `risk_score` 0-100
- Incidents created automatically when patterns detected
- IPs blocked after 2 HIGH violations
- Real-time WebSocket updates

---

## 🐛 TROUBLESHOOTING

### No incidents being created?
- Check correlation engine is active: `/intelligence/correlation/stats`
- Generate events that match correlation rules
- Check backend logs for correlation messages

### GeoIP not working?
- Check internet connection (uses ip-api.com)
- Private IPs (192.168.x.x) return "Private Network"
- Check backend logs for enrichment errors

### Anomaly detection not triggering?
- Need multiple events from same user/IP to build profile
- Check user profile: `/intelligence/user/{username}`
- Anomalies require 5+ historical events

---

## 📚 ADDITIONAL RESOURCES

- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

**Happy Testing! 🚀**
