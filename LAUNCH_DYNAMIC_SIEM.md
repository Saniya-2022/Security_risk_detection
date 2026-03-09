# 🚀 LAUNCH YOUR DYNAMIC MINI SIEM

## ⚡ Quick Launch (3 Steps)

### Step 1: Start Dynamic Backend
```bash
# Activate virtual environment
venv\Scripts\activate

# Start the LIVE system
start_dynamic_siem.bat
```

**You should see:**
```
🚀 Starting Mini SIEM Dynamic System...
✅ Phishing model loaded (95.2% accuracy)
✅ Login model loaded (91.2% accuracy)
✅ Network model loaded (94.4% accuracy)
✅ Malware model loaded (94.4% accuracy)
💓 Heartbeat started
🚀 Event Generator started - generating live security events
✅ Mini SIEM is now LIVE and generating events!
```

### Step 2: Start Frontend
```bash
# Open NEW terminal
cd frontend
npm start
```

### Step 3: Open Dashboard
Navigate to: **http://localhost:3000**

---

## ✅ What You'll See Immediately

### Dashboard Will Show:
1. **"LIVE" indicator** pulsing in green
2. **Real-time clock** ticking every second
3. **Alerts appearing** every 3-7 seconds automatically
4. **Statistics updating** in real-time
5. **Threat distribution** changing dynamically
6. **No manual refresh needed!**

### First Alert Should Appear Within 7 Seconds!

---

## 🎯 Key Features Now Working

### ✅ Continuous Event Generation
- Login attempts (brute force, normal)
- Network traffic (DoS, Probe, Normal)
- Email scans (phishing, legitimate)
- File scans (malware, safe)

### ✅ Real-Time ML Detection
- 4 trained models (91-95% accuracy)
- Instant predictions
- Confidence scores displayed

### ✅ Dynamic Risk Scoring
- Weighted scoring algorithm
- Severity classification
- Human-readable explanations

### ✅ WebSocket Live Updates
- Instant alert broadcasting
- Statistics updates
- IP block notifications
- Heartbeat every 30 seconds

### ✅ Automatic IP Blocking
- Tracks violations per IP
- Auto-blocks after 2 HIGH alerts
- Shows in Blocked IP panel

### ✅ Email Notifications
- Sent for HIGH severity alerts
- Includes full threat details
- Recommended actions

### ✅ Complete Source Information
Every alert shows:
- Source IP address
- Target user/email/file
- ML confidence score
- Detection method
- Risk factors

---

## 📊 Expected Behavior

### Event Generation Pattern
```
[3-7 sec] → Login Event → ML Detection → Risk Score → Alert → WebSocket → Dashboard
[3-7 sec] → Network Event → ML Detection → Risk Score → Alert → WebSocket → Dashboard
[3-7 sec] → Email Event → ML Detection → Risk Score → Alert → WebSocket → Dashboard
[3-7 sec] → Malware Event → ML Detection → Risk Score → Alert → WebSocket → Dashboard
```

### Alert Distribution (Approximate)
- **70%** LOW/MEDIUM severity (normal activity)
- **30%** HIGH severity (threats)
- **Login events**: 35%
- **Network events**: 35%
- **Email events**: 20%
- **Malware events**: 10%

### IP Blocking Trigger
```
IP 192.168.1.100 → HIGH alert (brute force)
                 ↓
IP 192.168.1.100 → HIGH alert (again)
                 ↓
🚫 IP AUTOMATICALLY BLOCKED
                 ↓
Notification sent via WebSocket
                 ↓
Appears in Blocked IP panel
```

---

## 🔍 Verify System is Working

### Check Backend Terminal
Should show logs like:
```
🚨 Alert generated: brute_force - HIGH
🚨 Alert generated: phishing - MEDIUM
🚨 Alert generated: dos - HIGH
📧 Email notification sent for alert 65a5f...
🚫 IP 192.168.1.100 has been blocked: Multiple HIGH severity violations
```

### Check Dashboard
- [ ] "LIVE" indicator is green and pulsing
- [ ] Clock is updating every second
- [ ] New alerts appearing automatically
- [ ] Statistics numbers increasing
- [ ] Threat distribution updating
- [ ] No console errors

### Check WebSocket
Open browser console (F12) and look for:
```
✅ WebSocket Connected
🔗 Connected to Mini SIEM
💓 Heartbeat received
```

---

## 🎮 Interactive Testing

### Watch Automatic Behavior
Just sit back and watch:
- Alerts flowing in
- Statistics updating
- IPs getting blocked
- Threat distribution changing

### Manual Controls
```bash
# Stop event generation
curl -X POST http://localhost:8000/control/stop-events

# Start event generation
curl -X POST http://localhost:8000/control/start-events

# Check system status
curl http://localhost:8000/system/status
```

---

## 📧 Email Notification Setup

If you want email notifications for HIGH alerts:

1. **Create Gmail App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Generate new app password

2. **Update .env file**
   ```env
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-16-char-app-password
   ```

3. **Restart backend**
   - Stop with CTRL+C
   - Run `start_dynamic_siem.bat` again

4. **Test**
   - Wait for a HIGH alert
   - Check your email inbox

---

## 🔧 Troubleshooting

### No Alerts Appearing?
1. Check backend terminal for "Event Generator started"
2. Verify no errors in backend logs
3. Check MongoDB connection
4. Restart backend

### WebSocket Not Connecting?
1. Ensure backend is on port 8000
2. Check browser console for errors
3. Try refreshing page
4. Check firewall settings

### Statistics Not Updating?
1. Verify WebSocket is connected ("LIVE" indicator)
2. Check browser console for errors
3. Refresh the page
4. Check backend logs

### Models Not Loading?
```bash
python backend/ml/retrain_models.py
```

---

## 📊 Performance Expectations

### Event Rate
- 1 event every 3-7 seconds
- ~10-20 events per minute
- ~600-1200 events per hour

### System Resources
- CPU: 10-30% idle, 40-60% active
- Memory: ~600MB
- Network: <1MB/sec
- Disk: ~1MB per 1000 alerts

### Response Times
- Event to Alert: <100ms
- Alert to Dashboard: <50ms
- Total latency: <150ms

---

## 🎯 Success Indicators

Your system is working perfectly if:

✅ Backend shows "Event Generator started"  
✅ Dashboard shows "LIVE" with pulse animation  
✅ Alerts appear every 3-7 seconds  
✅ Statistics update automatically  
✅ Threat distribution changes  
✅ IPs get blocked after violations  
✅ Email sent for HIGH alerts (if configured)  
✅ No errors in console  
✅ Clock updates every second  
✅ WebSocket heartbeat every 30 seconds  

---

## 🎉 You're Live!

Your Mini SIEM is now:
- ✅ Generating events continuously
- ✅ Processing through ML models
- ✅ Calculating risk scores
- ✅ Broadcasting alerts in real-time
- ✅ Updating dashboard automatically
- ✅ Blocking malicious IPs
- ✅ Sending email notifications
- ✅ Operating like a real SOC system

**Sit back and watch your SIEM in action!** 🛡️🤖🚀

---

## 📚 Documentation

- **Full Guide**: `DYNAMIC_SIEM_GUIDE.md`
- **API Examples**: `API_EXAMPLES.md`
- **Architecture**: `SYSTEM_ARCHITECTURE.md`
- **README**: `README.md`

---

## 🆘 Need Help?

1. Check `DYNAMIC_SIEM_GUIDE.md` for detailed information
2. Review backend logs for errors
3. Check browser console (F12)
4. Verify `.env` configuration
5. Test MongoDB connection

---

**Enjoy your fully dynamic, real-time Mini SIEM!** 🎊
