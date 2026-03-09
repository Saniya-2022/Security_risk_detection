# 🔌 Enterprise SIEM API Guide

Complete API reference for the Enterprise SIEM system.

---

## 📡 Base URL

```
http://localhost:8000
```

---

## 🎫 Incident Management API

### List Incidents

```http
GET /incidents?status={status}&severity={severity}&limit={limit}&skip={skip}
```

**Query Parameters:**
- `status` (optional): Filter by status (Open, Investigating, Resolved, Closed)
- `severity` (optional): Filter by severity (CRITICAL, HIGH, MEDIUM, LOW)
- `limit` (optional): Number of results (default: 50, max: 500)
- `skip` (optional): Skip N results for pagination

**Example:**
```bash
curl "http://localhost:8000/incidents?status=Open&severity=HIGH&limit=10"
```

**Response:**
```json
[
  {
    "incident_id": "uuid",
    "title": "Brute Force Attack Detected",
    "description": "...",
    "severity": "HIGH",
    "status": "Open",
    "related_alert_ids": ["alert1", "alert2"],
    "alert_count": 2,
    "assigned_analyst": null,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00",
    "mitre_tactic": "Credential Access",
    "mitre_technique": "T1110",
    "timeline": [...],
    "notes": []
  }
]
```

---

### Get Incident Statistics

```http
GET /incidents/stats
```

**Example:**
```bash
curl http://localhost:8000/incidents/stats
```

**Response:**
```json
{
  "total_incidents": 45,
  "by_status": {
    "Open": 12,
    "Investigating": 8,
    "Resolved": 20,
    "Closed": 5
  },
  "by_severity": {
    "CRITICAL": 5,
    "HIGH": 15,
    "MEDIUM": 20,
    "LOW": 5
  },
  "avg_resolution_time_hours": 4.5,
  "open_incidents": 12,
  "critical_incidents": 5
}
```

---

### Get Specific Incident

```http
GET /incidents/{incident_id}
```

**Example:**
```bash
curl http://localhost:8000/incidents/abc-123-def
```

---

### Update Incident Status

```http
PATCH /incidents/{incident_id}/status
Content-Type: application/json

{
  "status": "Investigating",
  "note": "Starting investigation"
}
```

**Example:**
```bash
curl -X PATCH http://localhost:8000/incidents/abc-123/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Investigating", "note": "Assigned to team"}'
```

**Valid Statuses:**
- `Open`
- `Investigating`
- `Resolved`
- `Closed`
- `False Positive`

---

### Assign Incident to Analyst

```http
PATCH /incidents/{incident_id}/assign
Content-Type: application/json

{
  "analyst": "john.doe@company.com",
  "note": "Assigning to senior analyst"
}
```

**Example:**
```bash
curl -X PATCH http://localhost:8000/incidents/abc-123/assign \
  -H "Content-Type: application/json" \
  -d '{"analyst": "john.doe@company.com", "note": "Expert in brute force attacks"}'
```

---

### Add Note to Incident

```http
POST /incidents/{incident_id}/notes
Content-Type: application/json

{
  "analyst": "john.doe@company.com",
  "note": "Investigated source IP - appears to be compromised server"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/incidents/abc-123/notes \
  -H "Content-Type: application/json" \
  -d '{"analyst": "john.doe", "note": "Found related alerts from same subnet"}'
```

---

### Create Incident Manually

```http
POST /incidents
Content-Type: application/json

{
  "title": "Suspicious Activity Detected",
  "description": "Multiple failed login attempts from unknown IP",
  "severity": "HIGH",
  "related_alert_ids": ["alert1", "alert2"],
  "mitre_tactic": "Credential Access",
  "mitre_technique": "T1110"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Manual Investigation Required",
    "description": "Unusual pattern detected",
    "severity": "MEDIUM",
    "related_alert_ids": []
  }'
```

---

## 🚨 Alert API (Enhanced)

### List Alerts

```http
GET /alerts?limit={limit}&severity={severity}&threat_type={threat_type}
```

**Query Parameters:**
- `limit` (optional): Number of results (default: 50, max: 500)
- `severity` (optional): Filter by severity (HIGH, MEDIUM, LOW)
- `threat_type` (optional): Filter by threat type (regex supported)

**Example:**
```bash
curl "http://localhost:8000/alerts?severity=HIGH&limit=20"
```

**Response includes:**
- ML detection results
- Threat intelligence enrichment
- Anomaly detection results
- MITRE ATT&CK mapping
- Risk analysis
- Recommended actions

---

### Get Alert Statistics

```http
GET /alerts/stats
```

**Example:**
```bash
curl http://localhost:8000/alerts/stats
```

**Response:**
```json
{
  "total_alerts": 1250,
  "by_severity": {
    "HIGH": 150,
    "MEDIUM": 450,
    "LOW": 650
  },
  "threat_distribution": [
    {"_id": "brute_force", "count": 45},
    {"_id": "phishing", "count": 38},
    {"_id": "dos", "count": 32}
  ],
  "active_connections": 2
}
```

---

### Get Specific Alert

```http
GET /alerts/{alert_id}
```

**Example:**
```bash
curl http://localhost:8000/alerts/507f1f77bcf86cd799439011
```

---

### Get Alert Timeline

```http
GET /alerts/timeline?hours={hours}
```

**Query Parameters:**
- `hours` (optional): Time window in hours (default: 24, max: 168)

**Example:**
```bash
curl "http://localhost:8000/alerts/timeline?hours=48"
```

---

## 🛡️ Security API

### List Blocked IPs

```http
GET /security/blocked-ips
```

**Example:**
```bash
curl http://localhost:8000/security/blocked-ips
```

**Response:**
```json
[
  {
    "ip_address": "192.168.1.100",
    "reason": "Auto-blocked: brute_force (Risk: 85.5)",
    "blocked_at": "2024-01-01T12:00:00",
    "last_blocked": "2024-01-01T12:00:00",
    "block_count": 3,
    "severity": "HIGH",
    "auto_blocked": true
  }
]
```

---

### Block IP Manually

```http
POST /security/block-ip?ip_address={ip}&reason={reason}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/security/block-ip?ip_address=192.168.1.50&reason=Manual%20block%20-%20suspicious%20activity"
```

---

### Unblock IP

```http
DELETE /security/unblock-ip/{ip_address}
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/security/unblock-ip/192.168.1.50
```

---

## ⚙️ System API

### System Status

```http
GET /system/status
```

**Example:**
```bash
curl http://localhost:8000/system/status
```

**Response:**
```json
{
  "status": "operational",
  "mode": "enterprise",
  "version": "2.0.0",
  "event_generator_running": true,
  "active_websocket_connections": 2,
  "email_service_enabled": true,
  "features": [
    "Real-time event generation",
    "Threat intelligence enrichment",
    "Anomaly detection",
    "MITRE ATT&CK mapping",
    "Advanced risk scoring",
    "Event correlation",
    "Incident management",
    "Auto IP blocking",
    "Email alerts"
  ]
}
```

---

### Health Check

```http
GET /system/health
```

**Example:**
```bash
curl http://localhost:8000/system/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-01T12:00:00"
}
```

---

## 🔌 WebSocket API

### Connect to WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('Connected to Enterprise SIEM');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  switch(message.type) {
    case 'connected':
      console.log('Welcome message:', message.message);
      break;
      
    case 'alert':
      console.log('New alert:', message.data);
      // Alert includes full enrichment
      break;
      
    case 'incident':
      console.log('New incident:', message.data);
      break;
      
    case 'ip_blocked':
      console.log('IP blocked:', message.data);
      break;
      
    case 'heartbeat':
      console.log('Heartbeat received');
      break;
  }
};
```

---

## 📊 Example Workflows

### Workflow 1: Monitor High-Risk Alerts

```bash
# Get high severity alerts
curl "http://localhost:8000/alerts?severity=HIGH&limit=10"

# Check if any incidents were created
curl http://localhost:8000/incidents?severity=HIGH

# Review blocked IPs
curl http://localhost:8000/security/blocked-ips
```

---

### Workflow 2: Investigate Incident

```bash
# Get incident details
curl http://localhost:8000/incidents/abc-123

# Assign to analyst
curl -X PATCH http://localhost:8000/incidents/abc-123/assign \
  -H "Content-Type: application/json" \
  -d '{"analyst": "analyst@company.com"}'

# Update status
curl -X PATCH http://localhost:8000/incidents/abc-123/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Investigating", "note": "Starting investigation"}'

# Add investigation notes
curl -X POST http://localhost:8000/incidents/abc-123/notes \
  -H "Content-Type: application/json" \
  -d '{"analyst": "analyst@company.com", "note": "Found related activity"}'

# Resolve incident
curl -X PATCH http://localhost:8000/incidents/abc-123/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Resolved", "note": "Threat mitigated"}'
```

---

### Workflow 3: Manual IP Management

```bash
# Block suspicious IP
curl -X POST "http://localhost:8000/security/block-ip?ip_address=10.0.0.50&reason=Suspicious%20scanning%20activity"

# Verify block
curl http://localhost:8000/security/blocked-ips

# Later: Unblock if false positive
curl -X DELETE http://localhost:8000/security/unblock-ip/10.0.0.50
```

---

## 📖 Interactive API Documentation

Visit **http://localhost:8000/docs** for:
- Interactive API testing
- Complete request/response schemas
- Try-it-out functionality
- Model definitions
- Authentication (if enabled)

---

## 🔐 Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## 💡 Tips

1. **Use pagination** for large result sets (limit + skip)
2. **Filter early** to reduce data transfer
3. **Monitor WebSocket** for real-time updates
4. **Check /system/health** for monitoring
5. **Use /docs** for interactive testing

---

## 🚀 Quick Test Commands

```bash
# Test system
curl http://localhost:8000/system/status

# Get recent alerts
curl http://localhost:8000/alerts?limit=5

# Get incidents
curl http://localhost:8000/incidents?limit=5

# Get stats
curl http://localhost:8000/incidents/stats
curl http://localhost:8000/alerts/stats

# Check blocked IPs
curl http://localhost:8000/security/blocked-ips
```

---

**For more details, visit: http://localhost:8000/docs**
