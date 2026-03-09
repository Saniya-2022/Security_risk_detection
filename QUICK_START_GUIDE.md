# 🚀 Mini SIEM - Quick Start Guide

## ⚡ 5-Minute Setup

### Prerequisites Check
- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] MongoDB Atlas account created
- [ ] Gmail account with App Password

---

## Step 1: Environment Configuration (2 minutes)

### Create `.env` file in project root:
```env
MONGO_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/security_risk_detection
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password
```

**Get Gmail App Password**: https://myaccount.google.com/apppasswords

---

## Step 2: Backend Setup (2 minutes)

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Generate datasets and train models
python setup_and_run.py
```

---

## Step 3: Start Services (1 minute)

### Terminal 1 - Backend:
```bash
uvicorn backend.api.main_enhanced:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm install    # First time only
npm start
```

---

## 🎉 You're Ready!

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Base**: http://localhost:8000

---

## 🧪 Test the System

### Run automated tests:
```bash
python test_all_endpoints.py
```

### Manual test (Phishing Detection):
```bash
curl -X POST "http://localhost:8000/detect/phishing" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "urgent@secure-bank.tk",
    "subject": "URGENT: Verify your account",
    "body": "Click here immediately",
    "num_links": 5,
    "suspicious_keywords": 4
  }'
```

---

## 📊 Dashboard Features

### What You'll See:
1. **Real-time Alert Feed** - Live security alerts as they happen
2. **Statistics Cards** - Total alerts, severity breakdown, blocked IPs
3. **Threat Distribution** - Chart showing attack types
4. **Blocked IP List** - Currently blocked addresses
5. **System Status** - Connection and health indicators

### Color Coding:
- 🔴 **RED** = HIGH severity (71-100 risk score)
- 🟡 **YELLOW** = MEDIUM severity (31-70 risk score)
- 🟢 **GREEN** = LOW severity (0-30 risk score)

---

## 🔍 Common Issues & Solutions

### Issue: "Cannot connect to MongoDB"
**Solution**: 
- Check MONGO_URI in `.env`
- Whitelist your IP in MongoDB Atlas
- Verify database user permissions

### Issue: "Email notifications not working"
**Solution**:
- Use Gmail App Password (not regular password)
- Check SENDER_EMAIL and SENDER_PASSWORD in `.env`
- Enable "Less secure app access" if needed

### Issue: "WebSocket connection failed"
**Solution**:
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify CORS settings allow localhost:3000

### Issue: "ML models not found"
**Solution**:
```bash
python backend/datasets/generate_datasets.py
python backend/ml/train_all_models.py
```

---

## 📝 Quick API Reference

### Detection Endpoints:
- `POST /detect/phishing` - Email phishing detection
- `POST /detect/login` - Login anomaly detection
- `POST /detect/network` - Network traffic classification
- `POST /detect/malware` - Malware file detection

### Management Endpoints:
- `GET /alerts` - Get all alerts
- `GET /alerts/stats` - Get statistics
- `GET /security/blocked-ips` - List blocked IPs
- `GET /system/status` - System health

### WebSocket:
- `WS /ws` - Real-time alert stream

---

## 🎓 Next Steps

1. **Explore the Dashboard**: Watch real-time alerts appear
2. **Run Tests**: Execute `test_all_endpoints.py`
3. **Check API Docs**: Visit http://localhost:8000/docs
4. **Read Full Docs**: See `PROJECT_DOCUMENTATION.md`
5. **Customize**: Modify risk scoring rules in `backend/risk_engine.py`

---

## 📞 Need Help?

- **API Documentation**: http://localhost:8000/docs
- **Full Documentation**: `PROJECT_DOCUMENTATION.md`
- **README**: `README.md`
- **Email**: sreeja.warangal834@gmail.com

---

## 🎯 Quick Test Scenarios

### Scenario 1: Phishing Email
```json
{
  "sender": "urgent@secure-bank.tk",
  "subject": "URGENT: Verify your account",
  "body": "Click here to verify",
  "num_links": 5,
  "suspicious_keywords": 6
}
```
**Expected**: HIGH severity alert

### Scenario 2: Brute Force Attack
```json
{
  "ip_address": "192.168.1.100",
  "username": "admin",
  "failed_attempts": 15,
  "time_of_login": 3,
  "country": "RU"
}
```
**Expected**: HIGH severity alert + IP may be blocked

### Scenario 3: DoS Attack
```json
{
  "ip_address": "203.0.113.50",
  "request_count_per_min": 1500,
  "port_number": 80,
  "packet_size": 50,
  "protocol": "TCP"
}
```
**Expected**: HIGH severity alert

---

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] MongoDB connection successful
- [ ] ML models loaded
- [ ] WebSocket connected (green indicator)
- [ ] Test alerts appearing in dashboard
- [ ] Email notifications working (for HIGH alerts)

---

**🎉 Congratulations! Your Mini SIEM is now operational!**

Monitor your security posture in real-time and let AI help detect threats automatically.
