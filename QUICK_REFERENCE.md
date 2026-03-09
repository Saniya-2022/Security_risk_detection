# 🚀 Enterprise SIEM - Quick Reference Card

## Start System

```bash
# Backend
START_ENTERPRISE_SIEM.bat

# Frontend
cd frontend
npm start
```

## Access Points

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/system/health

## Key Commands

### System Status
```bash
curl http://localhost:8000/system/status
```

### View Alerts
```bash
curl http://localhost:8000/alerts?limit=10
curl http://localhost:8000/alerts?severity=HIGH
```

### View Incidents
```bash
curl http://localhost:8000/incidents
curl http://localhost:8000/incidents/stats
```

### Blocked IPs
```bash
curl http://localhost:8000/security/blocked-ips
```

### Block IP
```bash
curl -X POST "http://localhost:8000/security/block-ip?ip_address=10.0.0.50&reason=Suspicious"
```

### Assign Incident
```bash
curl -X PATCH http://localhost:8000/incidents/{id}/assign \
  -H "Content-Type: application/json" \
  -d '{"analyst": "analyst@company.com"}'
```

### Update Incident Status
```bash
curl -X PATCH http://localhost:8000/incidents/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Investigating", "note": "Started investigation"}'
```

## Features at a Glance

| Feature | Endpoint | Description |
|---------|----------|-------------|
| Alerts | GET /alerts | Enhanced with threat intel |
| Incidents | GET /incidents | Full lifecycle management |
| Statistics | GET /alerts/stats | Real-time metrics |
| Blocked IPs | GET /security/blocked-ips | Auto + manual blocks |
| System Health | GET /system/health | Health check |
| API Docs | GET /docs | Interactive Swagger |

## Alert Structure

Every alert includes:
- ✅ ML detection results
- ✅ Threat intelligence (GeoIP, reputation)
- ✅ Anomaly detection results
- ✅ MITRE ATT&CK mapping
- ✅ Risk score (0-100)
- ✅ Recommended actions
- ✅ Incident ID (if created)

## Incident Workflow

1. **Created** - Automatically by correlation rules
2. **Assign** - PATCH /incidents/{id}/assign
3. **Investigate** - PATCH /incidents/{id}/status
4. **Add Notes** - POST /incidents/{id}/notes
5. **Resolve** - PATCH /incidents/{id}/status

## Correlation Rules

1. **Brute Force** - 5 failed + 1 success → Incident
2. **Escalation** - 3 MEDIUM → HIGH
3. **Suspicious Access** - 2 countries in 30 min
4. **Multi-Stage** - Probe + Exploit
5. **Repeated High** - 3 HIGH in 5 min

## Risk Scoring

```
Risk = (ML 50%) + (Severity 20%) + (Frequency 10%) + 
       (Threat Intel 10%) + (Anomaly 10%)
```

- **0-20**: INFO
- **20-40**: LOW
- **40-60**: MEDIUM
- **60-75**: HIGH
- **75-100**: CRITICAL

## Auto Actions

- **Risk > 60**: Email alert
- **Risk > 75**: Create incident + escalate
- **Risk > 80**: Block IP automatically

## MITRE Coverage

- **Initial Access**: T1190, T1566
- **Execution**: T1204, T1059
- **Credential Access**: T1110
- **Discovery**: T1046, T1087
- **Impact**: T1499, T1486
- **Persistence**: T1543
- **Lateral Movement**: T1210

## Anomaly Detection

- Unusual login times
- Rare IP for user
- Activity spikes
- Impossible travel

## Documentation

- **ENTERPRISE_UPGRADE_COMPLETE.md** - Full details
- **ENTERPRISE_API_GUIDE.md** - API reference
- **TEST_ENTERPRISE_FEATURES.md** - Testing guide
- **ENTERPRISE_SUMMARY.md** - Overview

## Troubleshooting

### No events generating
```bash
# Check logs for "Event generator started"
# Restart backend if needed
```

### WebSocket not connecting
```bash
# Check browser console (F12)
# Verify backend on port 8000
# Clear browser cache
```

### No incidents created
```bash
# Wait 2-3 minutes for correlation
# Check: curl http://localhost:8000/incidents
```

## Support

- **Logs**: Check backend terminal
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/system/health

---

**Quick Test:**
```bash
curl http://localhost:8000/system/status && \
curl http://localhost:8000/alerts?limit=1 && \
curl http://localhost:8000/incidents/stats
```

**All working? You're ready! 🚀**
