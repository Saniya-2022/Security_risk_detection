# 🚀 UNSW-NB15 IDS - Quick Start Guide

## ⚡ 5-Minute Setup

### 1️⃣ Download Dataset (2 minutes)

Visit: https://research.unsw.edu.au/projects/unsw-nb15-dataset

Download these 2 files:
- `UNSW_NB15_training-set.csv`
- `UNSW_NB15_testing-set.csv`

Place in: `backend/datasets/`

### 2️⃣ Run Setup (10-15 minutes)

**Windows:**
```bash
1_SETUP_UNSW_SYSTEM.bat
```

**Linux/Mac:**
```bash
python setup_unsw_system.py
```

This will:
- Install dependencies
- Train 3 ML models (Random Forest, XGBoost, Logistic Regression)
- Select best model automatically

### 3️⃣ Configure MongoDB

Edit `.env`:
```env
MONGODB_URI=mongodb+srv://your-connection-string
```

### 4️⃣ Start System

**Terminal 1 - Backend:**
```bash
2_START_UNSW_BACKEND.bat
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 5️⃣ Open Dashboard

http://localhost:3000

---

## ✅ Verification

You should see:

✅ Backend: "Started UNSW-NB15 streaming"  
✅ Dashboard: "LIVE" indicator pulsing  
✅ Alerts: Appearing every 1-2 seconds  
✅ Model Info: Banner showing accuracy  

---

## 🎯 What You Get

- **Real-time intrusion detection** using ML
- **9 attack types** detected (DoS, Exploit, Reconnaissance, etc.)
- **Automatic IP blocking** after 2 HIGH violations
- **Email alerts** for high-risk threats (risk > 70)
- **Live dashboard** with threat feed and statistics
- **85-95% accuracy** with trained models

---

## 📊 Key Features

| Feature | Description |
|---------|-------------|
| **ML Models** | Random Forest, XGBoost, Logistic Regression |
| **Dataset** | UNSW-NB15 (257,673 network flows) |
| **Features** | 49 network flow features |
| **Streaming** | 1-2 second intervals |
| **Storage** | MongoDB Atlas |
| **Alerts** | WebSocket real-time |
| **Dashboard** | React with live updates |

---

## 🔧 Quick Configuration

### Change Streaming Speed

Edit `backend/runtime/unsw_stream_service.py`:
```python
self.stream_interval = 1.5  # Change to 3.0 for slower
```

### Change IP Block Threshold

Edit `backend/api/main_unsw.py`:
```python
if high_count >= 2:  # Change to 3 or 5
```

### Change Email Alert Threshold

Edit `backend/api/main_unsw.py`:
```python
if alert['risk_score'] > 70:  # Change to 80 or 90
```

---

## 🐛 Common Issues

### "Dataset not found"
→ Download CSV files and place in `backend/datasets/`

### "Model not loaded"
→ Run training: `python backend/ml/train_unsw_models.py`

### "MongoDB connection failed"
→ Check `.env` has correct `MONGODB_URI`

### "No alerts appearing"
→ Check backend logs for "Started UNSW-NB15 streaming"

---

## 📚 Full Documentation

See `UNSW_NB15_GUIDE.md` for complete details.

---

**Ready to detect intrusions! 🛡️**
