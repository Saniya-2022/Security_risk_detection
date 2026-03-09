# WEBSOCKET TROUBLESHOOTING GUIDE
## Fix Dashboard Not Updating in Real-Time

---

## 🔍 PROBLEM: Dashboard Not Updating Continuously

If your dashboard is not showing real-time updates when you open it, follow these steps:

---

## ✅ STEP 1: Check Backend is Running

### Open Terminal 1 and run:
```bash
cd C:\Security_Risk_detection
venv\Scripts\activate
uvicorn backend.api.main_dynamic:app --reload --host 0.0.0.0 --port 8000
```

### You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Will watch for changes in these directories
🚀 Starting Mini SIEM Dynamic System...
✅ Mini SIEM is now LIVE and generating events!
```

### ⚠️ If you see errors:
- Make sure you're in the correct directory
- Make sure virtual environment is activated
- Check if port 8000 is already in use

---

## ✅ STEP 2: Check Frontend is Running

### Open Terminal 2 and run:
```bash
cd C:\Security_Risk_detection\frontend
npm start
```

### You should see:
```
Compiled successfully!
You can now view frontend in the browser.
Local:            http://localhost:3000
```

### ⚠️ If you see errors:
- Run `npm install` first if node_modules is missing
- Check if port 3000 is already in use

---

## ✅ STEP 3: Check WebSocket Connection in Browser

### Open Browser Console (F12):

**Look for these messages:**
```
✅ WebSocket Connected
🔗 Connected to Mini SIEM
💓 Heartbeat received
```

**If you see:**
```
❌ WebSocket Disconnected
WebSocket error: ...
```

**Then the backend is not running or not accessible!**

---

## ✅ STEP 4: Verify Events are Being Generated

### In Backend Terminal, you should see:
```
🚨 Alert generated: phishing - HIGH
🚨 Alert generated: brute_force - MEDIUM
🚨 Alert generated: normal_login - LOW
```

**If you DON'T see these messages:**
- The event generator is not running
- Check if `main_dynamic.py` is being used (not `main.py`)

---

## ✅ STEP 5: Test WebSocket Manually

### Open Browser Console and run:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onopen = () => console.log('Connected!');
ws.onmessage = (e) => console.log('Message:', JSON.parse(e.data));
ws.onerror = (e) => console.error('Error:', e);
```

**You should see:**
```
Connected!
Message: {type: "connected", message: "Connected to Mini SIEM", ...}
Message: {type: "alert", data: {...}, ...}
Message: {type: "statistics", data: {...}, ...}
```

---

## 🔧 COMMON FIXES

### Fix 1: Backend Not Running
```bash
# Stop any running backend
# Press Ctrl+C in backend terminal

# Start correct backend
cd C:\Security_Risk_detection
venv\Scripts\activate
uvicorn backend.api.main_dynamic:app --reload --host 0.0.0.0 --port 8000
```

### Fix 2: Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Restart backend
uvicorn backend.api.main_dynamic:app --reload --host 0.0.0.0 --port 8000
```

### Fix 3: WebSocket URL Wrong
Check `frontend/src/Dashboard.js` line 42:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

Should be `ws://localhost:8000/ws` (NOT `wss://` or different port)

### Fix 4: CORS Issues
Check backend terminal for CORS errors. If you see them, the backend CORS is already configured correctly in `main_dynamic.py`.

### Fix 5: Browser Cache
```
1. Press Ctrl+Shift+R (hard refresh)
2. Or clear browser cache
3. Or open in Incognito mode
```

---

## 🎯 QUICK TEST CHECKLIST

Run these commands in order:

### Terminal 1 (Backend):
```bash
cd C:\Security_Risk_detection
venv\Scripts\activate
uvicorn backend.api.main_dynamic:app --reload --host 0.0.0.0 --port 8000
```
✅ Wait for "Mini SIEM is now LIVE"

### Terminal 2 (Frontend):
```bash
cd C:\Security_Risk_detection\frontend
npm start
```
✅ Wait for "Compiled successfully"

### Browser:
1. Open http://localhost:3000
2. Press F12 (open console)
3. Look for "✅ WebSocket Connected"
4. Watch for new alerts appearing every 3-7 seconds

---

## 📊 WHAT YOU SHOULD SEE

### Backend Terminal:
```
🚀 Event Generator started - generating live security events
🚨 Alert generated: phishing - HIGH
🚨 Alert generated: brute_force - MEDIUM
🚨 Alert generated: normal_login - LOW
✅ New WebSocket connection. Total: 1
```

### Browser Console:
```
✅ WebSocket Connected
🔗 Connected to Mini SIEM
💓 Heartbeat received
```

### Dashboard:
- New alerts appearing every 3-7 seconds
- Statistics updating automatically
- Total alerts count increasing
- Severity distribution changing
- No need to refresh page

---

## 🚨 STILL NOT WORKING?

### Check Event Generator Status:

**Open new terminal:**
```bash
cd C:\Security_Risk_detection
venv\Scripts\activate
python
```

**In Python shell:**
```python
from backend.event_generator import event_generator
print(f"Running: {event_generator.running}")
```

**Should print:** `Running: True`

**If False, restart backend!**

---

## 🔍 DEBUG MODE

### Add this to Dashboard.js (line 50, after ws.onmessage):
```javascript
ws.onmessage = (event) => {
  console.log('📨 WebSocket Message:', event.data); // ADD THIS LINE
  const message = JSON.parse(event.data);
  // ... rest of code
};
```

**Now you'll see every WebSocket message in console!**

---

## ✅ VERIFICATION STEPS

### 1. Backend Health Check:
```bash
curl http://localhost:8000/system/health
```
**Should return:** `{"status":"healthy","database":"connected",...}`

### 2. WebSocket Endpoint Check:
```bash
curl http://localhost:8000/
```
**Should return:** `{"message":"Mini SIEM v2.1 - Dynamic Real-Time Security Monitoring",...}`

### 3. Recent Alerts Check:
```bash
curl http://localhost:8000/alerts?limit=5
```
**Should return:** Array of recent alerts

---

## 🎯 EXPECTED BEHAVIOR

**When Everything Works:**

1. **Backend starts** → Event generator begins
2. **Events generated** every 3-7 seconds
3. **Alerts created** and saved to MongoDB
4. **WebSocket broadcasts** alerts to all connected clients
5. **Dashboard receives** alerts via WebSocket
6. **UI updates** automatically without refresh
7. **Statistics update** in real-time
8. **New alerts appear** at the top of the list

**Timeline:**
- 0s: Open dashboard
- 0s: WebSocket connects
- 3-7s: First alert appears
- 6-14s: Second alert appears
- Continuous updates every 3-7 seconds

---

## 📞 FINAL CHECKLIST

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Browser console shows "WebSocket Connected"
- [ ] Backend terminal shows "Alert generated" messages
- [ ] Dashboard shows alerts appearing automatically
- [ ] No need to refresh page
- [ ] Statistics updating in real-time

**If ALL checked ✅ → WebSocket is working!**

---

## 🔧 EMERGENCY FIX

If nothing works, try this complete restart:

```bash
# 1. Stop everything (Ctrl+C in all terminals)

# 2. Kill all Python processes
taskkill /F /IM python.exe

# 3. Kill all Node processes
taskkill /F /IM node.exe

# 4. Wait 5 seconds

# 5. Start backend
cd C:\Security_Risk_detection
venv\Scripts\activate
uvicorn backend.api.main_dynamic:app --reload --host 0.0.0.0 --port 8000

# 6. Wait for "Mini SIEM is now LIVE"

# 7. Start frontend (new terminal)
cd C:\Security_Risk_detection\frontend
npm start

# 8. Open browser to http://localhost:3000

# 9. Press F12 and check console
```

---

## 📝 NOTES

- WebSocket updates happen automatically
- No page refresh needed
- Events generate every 3-7 seconds
- Dashboard should show new alerts continuously
- If you don't see updates, backend is not running or WebSocket is not connected
