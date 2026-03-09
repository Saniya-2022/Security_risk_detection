# 🧪 Enterprise SIEM Testing Guide

Step-by-step guide to test all enterprise features.

---

## 🚀 Prerequisites

1. **Start Enterprise Backend:**
   ```bash
   START_ENTERPRISE_SIEM.bat
   ```
   OR
   ```bash
   venv\Scripts\activate
   uvicorn backend.api.main_enterprise:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Open Browser:**
   - Dashboard: http://localhost:3000
   - API Docs: http://localhost:8000/docs

---

## ✅ Test 1: System Health Check

### Expected: System is operational

```bash
curl http://localhost:8000/system/status
```

**Should show:**
```json
{
  "status": "operational",
  "mode": "enterprise",
  "version": "2.0.0",
  "event_generator_running": true,
  "features": [...]
}
```

✅ **Pass if:** All features listed, event_generator_running = true

---

## ✅ Test 2: Event Generation

### Expected: Events generate automatically every 3-7 seconds

**Watch backend logs for:**
```
INFO: Processing event: login
INFO: Risk calculated: 45.23 (MEDIUM)
INFO: Alert processed successfully
```

**Check dashboard:**
- New alerts appear automatically
- Counter increases
- No page refresh needed

✅ **Pass if:** Alerts appear every 3-7 seconds automatically

---

## ✅ Test 3: Threat Intelligence Enrichment

### Expected: All alerts have GeoIP and threat intel data

```bash
curl http://localhost:8000/alerts?limit=1
```

**Check response for:**
```json
{
  "threat_intelligence": {
    "country": "US",
    "city": "New York",
    "asn": "AS15169",
    "is_blacklisted": false,
    "reputation_score": 85,
    "threat_level": "clean"
  }
}
```

✅ **Pass if:** Every alert has threat_intelligence field with country, reputation_score

---

## ✅ Test 4: MITRE ATT&CK Mapping

### Expected: Threats mapped to MITRE framework

```bash
curl http://localhost:8000/alerts?limit=5
```

**Check for:**
```json
{
  "mitre_attack": {
    "tactic": "Credential Access",
    "technique_id": "T1110",
    "technique_name": "Brute Force",
    "description": "..."
  }
}
```

✅ **Pass if:** Alerts have mitre_attack with tactic and technique_id

---

## ✅ Test 5: Anomaly Detection

### Expected: Behavioral anomalies detected

**Wait for alerts, then check:**
```bash
curl http://localhost:8000/alerts?limit=10
```

**Look for:**
```json
{
  "anomaly_detection": {
    "is_anomaly": true,
    "anomaly_score": 0.8,
    "anomaly_type": ["unusual_login_time", "rare_ip_for_user"],
    "anomaly_details": [...]
  }
}
```

✅ **Pass if:** Some alerts have is_anomaly: true with anomaly_type

---

## ✅ Test 6: Advanced Risk Scoring

### Expected: Risk scores calculated with multiple factors

```bash
curl http://localhost:8000/alerts?limit=5
```

**Check for:**
```json
{
  "risk_score": 78.5,
  "risk_level": "HIGH",
  "risk_analysis": {
    "risk_score": 78.5,
    "risk_level": "HIGH",
    "components": {
      "ml_confidence": 47.5,
      "severity": 20.0,
      "frequency": 8.0,
      "threat_intelligence": 1.5,
      "anomaly": 8.0
    },
    "should_escalate": true,
    "should_alert": true
  }
}
```

✅ **Pass if:** Alerts have risk_score, risk_level, and risk_analysis.components

---

## ✅ Test 7: Auto-Escalation

### Expected: MEDIUM alerts escalate to HIGH when risk > 75

**Watch backend logs for:**
```
WARNING: Alert auto-escalated to HIGH: login
```

**Check alert:**
```json
{
  "severity": "HIGH",
  "auto_escalated": true,
  "risk_score": 78.5
}
```

✅ **Pass if:** Some alerts show auto_escalated: true

---

## ✅ Test 8: Event Correlation & Incident Creation

### Expected: Incidents created automatically when correlation rules match

**Wait 2-3 minutes for events to accumulate, then:**

```bash
curl http://localhost:8000/incidents
```

**Should see incidents like:**
```json
{
  "incident_id": "uuid",
  "title": "Brute Force Attack Detected - 192.168.1.100",
  "description": "Detected 5 failed login attempts followed by successful login",
  "severity": "HIGH",
  "status": "Open",
  "correlation_rule": "brute_force_pattern",
  "related_alert_ids": ["alert1", "alert2", "alert3"],
  "alert_count": 3
}
```

**Backend logs should show:**
```
INFO: Correlation rule triggered: Brute Force Attack Pattern
WARNING: Incident created: uuid - Brute Force Attack Detected
```

✅ **Pass if:** Incidents are created automatically with related_alert_ids

---

## ✅ Test 9: Incident Management

### Expected: Full incident lifecycle works

**1. List incidents:**
```bash
curl http://localhost:8000/incidents
```

**2. Get incident stats:**
```bash
curl http://localhost:8000/incidents/stats
```

**3. Assign incident (replace {id} with actual incident_id):**
```bash
curl -X PATCH http://localhost:8000/incidents/{id}/assign \
  -H "Content-Type: application/json" \
  -d '{"analyst": "john.doe@company.com", "note": "Investigating"}'
```

**4. Update status:**
```bash
curl -X PATCH http://localhost:8000/incidents/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Investigating", "note": "Started investigation"}'
```

**5. Add note:**
```bash
curl -X POST http://localhost:8000/incidents/{id}/notes \
  -H "Content-Type: application/json" \
  -d '{"analyst": "john.doe", "note": "Found related activity"}'
```

**6. Verify timeline updated:**
```bash
curl http://localhost:8000/incidents/{id}
```

✅ **Pass if:** All operations succeed and timeline shows all actions

---

## ✅ Test 10: Auto IP Blocking

### Expected: IPs auto-blocked when risk > 80

**Watch backend logs for:**
```
WARNING: IP auto-blocked: 192.168.1.100 (Risk: 85.50)
```

**Check blocked IPs:**
```bash
curl http://localhost:8000/security/blocked-ips
```

**Should see:**
```json
[
  {
    "ip_address": "192.168.1.100",
    "reason": "Auto-blocked: brute_force (Risk: 85.50)",
    "auto_blocked": true,
    "block_count": 1
  }
]
```

✅ **Pass if:** High-risk IPs appear in blocked list with auto_blocked: true

---

## ✅ Test 11: Manual IP Blocking

### Expected: Can manually block/unblock IPs

**1. Block IP:**
```bash
curl -X POST "http://localhost:8000/security/block-ip?ip_address=10.0.0.99&reason=Manual%20test"
```

**2. Verify blocked:**
```bash
curl http://localhost:8000/security/blocked-ips
```

**3. Unblock IP:**
```bash
curl -X DELETE http://localhost:8000/security/unblock-ip/10.0.0.99
```

**4. Verify unblocked:**
```bash
curl http://localhost:8000/security/blocked-ips
```

✅ **Pass if:** IP appears after block, disappears after unblock

---

## ✅ Test 12: WebSocket Real-Time Updates

### Expected: Dashboard receives real-time updates

**Open browser console (F12) and check for:**
```
✅ WebSocket Connected
💓 Heartbeat received
🔗 Connected to Mini SIEM
```

**Watch for messages:**
- New alerts appear without refresh
- Incident notifications
- IP block notifications
- "LIVE" indicator pulsing

✅ **Pass if:** Dashboard updates in real-time, no page refresh needed

---

## ✅ Test 13: Email Alerts (if configured)

### Expected: Emails sent for high-risk alerts

**Check backend logs for:**
```
INFO: Alert email sent for brute_force
```

**If email configured, check inbox for:**
- Subject: "🚨 HIGH Security Alert - brute_force"
- Body includes:
  - Risk score
  - Threat intelligence
  - MITRE mapping
  - Recommended actions

✅ **Pass if:** Email logs appear (or emails received if SMTP configured)

---

## ✅ Test 14: Recommended Actions

### Expected: Alerts include actionable recommendations

```bash
curl http://localhost:8000/alerts?severity=HIGH&limit=1
```

**Check for:**
```json
{
  "recommended_actions": [
    "Create incident immediately",
    "Send email alert to SOC team",
    "Consider blocking source IP",
    "Escalate to senior analyst",
    "Enable enhanced monitoring"
  ]
}
```

✅ **Pass if:** High-risk alerts have 3+ recommended actions

---

## ✅ Test 15: Alert Deduplication

### Expected: Duplicate alerts are filtered

**Backend logs should show:**
```
INFO: Duplicate alert detected - skipping
```

**Verify:**
- Same threat from same IP within 5 minutes = deduplicated
- Alert count doesn't spike unnaturally

✅ **Pass if:** Logs show deduplication working

---

## ✅ Test 16: Dashboard Features

### Expected: Dashboard shows all enterprise features

**Check dashboard for:**
1. ✅ Real-time alert feed
2. ✅ Risk scores visible
3. ✅ MITRE ATT&CK data (if displayed)
4. ✅ Threat intelligence (country, reputation)
5. ✅ Anomaly indicators
6. ✅ Blocked IPs list
7. ✅ Live clock
8. ✅ "LIVE" indicator pulsing
9. ✅ Statistics updating
10. ✅ No console errors

✅ **Pass if:** All features visible and working

---

## ✅ Test 17: API Documentation

### Expected: Swagger docs accessible and complete

**Visit:** http://localhost:8000/docs

**Check for:**
- All incident endpoints
- All alert endpoints
- All security endpoints
- Try-it-out functionality works
- Schemas are complete

✅ **Pass if:** Can test endpoints directly from /docs

---

## ✅ Test 18: Statistics Accuracy

### Expected: Stats reflect actual data

```bash
# Get alert stats
curl http://localhost:8000/alerts/stats

# Get incident stats
curl http://localhost:8000/incidents/stats
```

**Verify:**
- Total counts match database
- Severity breakdown accurate
- Threat distribution correct

✅ **Pass if:** Numbers make sense and update in real-time

---

## ✅ Test 19: Performance

### Expected: System handles load efficiently

**Monitor for 5 minutes:**
- Backend CPU usage
- Memory usage
- Response times
- WebSocket stability

**Check:**
```bash
# Should respond quickly
time curl http://localhost:8000/alerts?limit=100
```

✅ **Pass if:** Response time < 1 second, no memory leaks

---

## ✅ Test 20: Error Handling

### Expected: Graceful error handling

**Test invalid requests:**
```bash
# Invalid incident ID
curl http://localhost:8000/incidents/invalid-id

# Invalid status
curl -X PATCH http://localhost:8000/incidents/abc/status \
  -H "Content-Type: application/json" \
  -d '{"status": "INVALID"}'
```

✅ **Pass if:** Returns proper error messages, doesn't crash

---

## 📊 Test Results Summary

| Test | Feature | Status |
|------|---------|--------|
| 1 | System Health | ⬜ |
| 2 | Event Generation | ⬜ |
| 3 | Threat Intelligence | ⬜ |
| 4 | MITRE Mapping | ⬜ |
| 5 | Anomaly Detection | ⬜ |
| 6 | Risk Scoring | ⬜ |
| 7 | Auto-Escalation | ⬜ |
| 8 | Event Correlation | ⬜ |
| 9 | Incident Management | ⬜ |
| 10 | Auto IP Blocking | ⬜ |
| 11 | Manual IP Blocking | ⬜ |
| 12 | WebSocket Updates | ⬜ |
| 13 | Email Alerts | ⬜ |
| 14 | Recommended Actions | ⬜ |
| 15 | Deduplication | ⬜ |
| 16 | Dashboard Features | ⬜ |
| 17 | API Documentation | ⬜ |
| 18 | Statistics | ⬜ |
| 19 | Performance | ⬜ |
| 20 | Error Handling | ⬜ |

---

## 🎯 Quick Validation Script

Run all tests at once:

```bash
# System check
echo "Test 1: System Status"
curl -s http://localhost:8000/system/status | grep "operational"

# Alerts check
echo "Test 2: Alerts"
curl -s http://localhost:8000/alerts?limit=1 | grep "threat_intelligence"

# Incidents check
echo "Test 3: Incidents"
curl -s http://localhost:8000/incidents/stats | grep "total_incidents"

# Security check
echo "Test 4: Blocked IPs"
curl -s http://localhost:8000/security/blocked-ips | grep "ip_address"

echo "✅ All basic tests passed!"
```

---

## 🐛 Troubleshooting

### No events generating
- Check backend logs for "Event generator started"
- Verify MongoDB connection
- Restart backend

### No incidents created
- Wait 2-3 minutes for correlation
- Check alert count (need multiple alerts)
- Verify correlation rules in logs

### WebSocket not connecting
- Check browser console for errors
- Verify backend running on port 8000
- Clear browser cache

### Missing enrichment data
- Check internet connection (for GeoIP)
- Verify requests library installed
- Check backend logs for errors

---

## ✅ Success Criteria

**System is working correctly if:**
1. ✅ Events generate automatically
2. ✅ All alerts have threat intelligence
3. ✅ MITRE mappings present
4. ✅ Risk scores calculated
5. ✅ Incidents created automatically
6. ✅ IPs auto-blocked for high risk
7. ✅ WebSocket updates in real-time
8. ✅ API endpoints respond correctly
9. ✅ Dashboard shows all features
10. ✅ No errors in logs

---

**Happy Testing! 🚀**
