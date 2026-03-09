# 📍 Location-Based Alerts Analysis

## ✅ System Status
- Backend: **RUNNING** on http://localhost:8000
- Events generating: **YES** (every 3-7 seconds)
- Location data: **PRESENT** in alerts

---

## 🌍 Location Data Found in Alerts

### Alert 1: Login from France
```json
{
  "event_type": "Login Attempt",
  "threat_type": "normal_login",
  "source_ip": "10.0.0.30",
  "target_user": "root",
  "country": "FR",  // ← France
  "timestamp": "2026-02-22T18:04:06"
}
```

### Alert 2: Login from Germany  
```json
{
  "event_type": "Login Attempt",
  "threat_type": "normal_login",
  "source_ip": "10.0.0.30",
  "target_user": "root",
  "country": "DE",  // ← Germany
  "timestamp": "2026-02-22T18:03:57"
}
```

---

## 🔍 Analysis

**Same User, Different Countries:**
- User: `root`
- IP: `10.0.0.30` (same IP)
- Countries: `FR` (France) and `DE` (Germany)
- Time difference: ~9 seconds

**Note:** The current `main_dynamic.py` API does NOT have the enterprise correlation engine, so it won't automatically create incidents for different country access.

---

## 🎯 To Enable Location-Based Incident Creation

You need to use the **Enterprise API** (`main_enterprise.py`) which includes:

1. ✅ Event Correlation Engine
2. ✅ Threat Intelligence Enrichment (GeoIP)
3. ✅ Automatic Incident Creation
4. ✅ MITRE ATT&CK Mapping
5. ✅ Advanced Risk Scoring

### The Enterprise API will:
- Detect when same user accesses from 2+ countries within 30 minutes
- Automatically create an incident
- Title: "Suspicious Access Pattern - {username}"
- Description: "User accessed from X different countries: US, CN, etc."

---

## 🚀 How to Switch to Enterprise API

### Option 1: Fix Motor Package (Recommended)

The enterprise API needs the `motor` package for async MongoDB. The issue is it's not being found in the subprocess.

**Try this:**
```powershell
# In your terminal
venv\Scripts\activate
pip uninstall motor pymongo -y
pip install pymongo==4.5.0 motor==3.3.2
```

Then start enterprise:
```powershell
uvicorn backend.api.main_enterprise:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Use Current System

The current `main_dynamic.py` has:
- ✅ Real-time event generation
- ✅ Location data in alerts (country field)
- ✅ ML detection
- ✅ Risk scoring
- ❌ NO automatic incident creation for location patterns

You can manually check for location patterns by querying alerts:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/alerts?limit=50" | 
  ConvertTo-Json -Depth 10 | 
  Select-String -Pattern "country"
```

---

## 📊 Current Alerts Summary

From the 10 most recent alerts:

| Event Type | User | IP | Country | Timestamp |
|------------|------|----|---------| ----------|
| Login | root | 10.0.0.30 | FR | 18:04:06 |
| Login | root | 10.0.0.30 | DE | 18:03:57 |

**Pattern Detected:** Same user from 2 different countries!

---

## 🎯 Recommendation

To get full enterprise features including automatic location-based incident creation:

1. Fix the motor package installation issue
2. Switch to `main_enterprise.py`
3. The correlation engine will automatically detect and create incidents

**Current Status:**
- ✅ Location data IS being generated
- ✅ Alerts contain country information
- ❌ Automatic correlation NOT active (need enterprise API)

---

## 📝 Commands to Check Location Alerts

### Get all alerts with location data:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/alerts?limit=50"
```

### Filter for login events:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/alerts?limit=50" | 
  Where-Object { $_.event_type -eq "Login Attempt" }
```

### Check for same user, different countries:
```powershell
$alerts = Invoke-RestMethod -Uri "http://localhost:8000/alerts?limit=100"
$logins = $alerts | Where-Object { $_.event_type -eq "Login Attempt" }
$logins | Group-Object target_user | Where-Object { $_.Count -gt 1 }
```

---

**System is working! Location data is present. Enterprise correlation engine needed for automatic incident creation.**
