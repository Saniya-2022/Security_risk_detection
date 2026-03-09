# 🚀 START HERE - Mini SIEM Quick Launch

## ✅ Setup Complete!

Your datasets are generated and ML models are trained. Now let's start the system!

---

## 📋 Step-by-Step Launch

### Step 1: Start Backend Server

**Option A - Using batch file (Recommended):**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Run the startup script
start_backend.bat
```

**Option B - Manual command:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Start the enhanced API
uvicorn backend.api.main_enhanced:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
✅ Phishing model loaded
✅ Login model loaded
✅ Network model loaded
✅ Malware model loaded
INFO:     Application startup complete.
```

### Step 2: Start Frontend Dashboard

**Open a NEW terminal window:**
```bash
cd frontend
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

### Step 3: Access the System

- **Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Base**: http://localhost:8000

---

## 🧪 Test the System

**Open a THIRD terminal window:**
```bash
# Activate virtual environment
venv\Scripts\activate

# Run comprehensive tests
python test_all_endpoints.py
```

This will:
- Test all detection endpoints
- Generate sample alerts
- Show them appearing in real-time on the dashboard
- Test IP blocking functionality

---

## ✅ Verification Checklist

After starting both servers, verify:

- [ ] Backend shows "✅ Phishing model loaded" (and 3 more)
- [ ] Frontend opens at http://localhost:3000
- [ ] Dashboard shows "Live" indicator (green dot)
- [ ] No console errors in browser
- [ ] API docs accessible at http://localhost:8000/docs

---

## 🎯 What You Should See

### Backend Terminal:
```
✅ Phishing model loaded
✅ Login model loaded
✅ Network model loaded
✅ Malware model loaded
INFO:     Application startup complete.
```

### Frontend Dashboard:
- Dark themed SOC dashboard
- "Live" connection indicator (green)
- Statistics cards showing 0 alerts initially
- Empty alert feed
- System status showing "operational"

### After Running Tests:
- Alerts appearing in real-time
- Statistics updating automatically
- Color-coded severity indicators
- Blocked IPs appearing (if HIGH alerts generated)

---

## 🔧 Troubleshooting

### Issue: "Module not found" errors
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Backend shows "⚠️ model not found"
**Solution:**
```bash
python backend/datasets/generate_datasets.py
python backend/ml/train_all_models.py
```

### Issue: Frontend won't start
**Solution:**
```bash
cd frontend
npm install
npm start
```

### Issue: WebSocket not connecting
**Solution:**
- Make sure backend is running on port 8000
- Check browser console for errors
- Verify no firewall blocking WebSocket

### Issue: MongoDB connection error
**Solution:**
- Check `.env` file has correct MONGO_URI
- Verify MongoDB Atlas network access allows your IP
- Test connection: `python verify_installation.py`

---

## 📊 Quick Test Commands

### Test Phishing Detection:
```bash
curl -X POST "http://localhost:8000/detect/phishing" \
  -H "Content-Type: application/json" \
  -d "{\"sender\":\"urgent@secure-bank.tk\",\"subject\":\"URGENT: Verify account\",\"body\":\"Click here\",\"num_links\":5,\"suspicious_keywords\":4}"
```

### Test Login Anomaly:
```bash
curl -X POST "http://localhost:8000/detect/login" \
  -H "Content-Type: application/json" \
  -d "{\"ip_address\":\"192.168.1.100\",\"username\":\"admin\",\"failed_attempts\":15,\"time_of_login\":3,\"country\":\"RU\"}"
```

### Get All Alerts:
```bash
curl http://localhost:8000/alerts
```

### Get System Status:
```bash
curl http://localhost:8000/system/status
```

---

## 🎉 Success Indicators

You'll know everything is working when:

1. ✅ Backend shows all 4 models loaded
2. ✅ Frontend dashboard displays with "Live" indicator
3. ✅ Test script generates alerts that appear instantly
4. ✅ Statistics update in real-time
5. ✅ No errors in any terminal
6. ✅ API docs work at /docs

---

## 📚 Next Steps

Once everything is running:

1. **Explore the Dashboard**: Navigate through different sections
2. **Run Tests**: Execute `python test_all_endpoints.py`
3. **Check API Docs**: Visit http://localhost:8000/docs
4. **Read Documentation**: See `README.md` for full details
5. **Customize**: Modify risk scoring in `backend/risk_engine.py`

---

## 🆘 Need Help?

- **Full Documentation**: See `README.md`
- **API Examples**: See `API_EXAMPLES.md`
- **Architecture**: See `SYSTEM_ARCHITECTURE.md`
- **Troubleshooting**: See `QUICK_START_GUIDE.md`

---

## 🎯 Important Notes

### Use the Enhanced API!
❌ **DON'T USE**: `uvicorn backend.api.main:app`
✅ **USE THIS**: `uvicorn backend.api.main_enhanced:app`

The enhanced API includes:
- All 4 ML models
- WebSocket support
- IP blocking
- Email notifications
- Complete risk scoring

### Frontend Update
The frontend has been updated to use the new Dashboard component with:
- Real-time WebSocket updates
- Professional SOC theme
- Live statistics
- Blocked IP management

---

**Ready to launch? Follow Step 1 above!** 🚀
