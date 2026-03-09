# 🛡️ UNSW-NB15 Intrusion Detection System - Complete Guide

## 📋 Overview

This is an enterprise-grade, real-time intrusion detection system using the UNSW-NB15 dataset and machine learning. The system streams network traffic data, analyzes it with trained ML models, and provides instant alerts through a live dashboard.

---

## 🎯 Key Features

### ✅ Machine Learning
- **3 ML Models**: Random Forest, Logistic Regression, XGBoost
- **Automatic Model Selection**: Best performing model chosen automatically
- **Real-World Dataset**: UNSW-NB15 with 49 features
- **High Accuracy**: 85-95% detection accuracy
- **Class Balancing**: SMOTE for handling imbalanced data

### ✅ Real-Time Detection
- **Live Streaming**: Test dataset streamed at 1-2 second intervals
- **WebSocket Updates**: Instant alert delivery to dashboard
- **Risk Scoring**: 0-100 risk score based on attack type, confidence, frequency
- **Attack Classification**: 9 attack categories (DoS, Exploit, Reconnaissance, etc.)

### ✅ Security Features
- **Automatic IP Blocking**: Block IPs after 2+ HIGH severity violations
- **Email Alerts**: Automatic notifications for risk > 70
- **MongoDB Storage**: All alerts stored with full metadata
- **Threat Intelligence**: Attack distribution and top source IPs

### ✅ Enterprise Dashboard
- **Live Threat Feed**: Real-time scrolling alerts
- **Severity Color Coding**: Visual distinction (RED/YELLOW/GREEN)
- **Risk Visualization**: Risk scores and ML confidence
- **Attack Distribution**: Charts showing threat types
- **Top Source IPs**: Most active attackers
- **System Status**: Model info, streaming status, connections

---

## 📥 Installation & Setup

### Step 1: Download UNSW-NB15 Dataset

1. Visit: https://research.unsw.edu.au/projects/unsw-nb15-dataset
2. Download these files:
   - `UNSW_NB15_training-set.csv` (~175,341 rows)
   - `UNSW_NB15_testing-set.csv` (~82,332 rows)
3. Place both files in: `backend/datasets/`

### Step 2: Install Dependencies

```bash
# Activate virtual environment
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

**New Dependencies Added:**
- `xgboost==2.0.3` - XGBoost ML model
- `imbalanced-learn==0.12.0` - SMOTE for class balancing

### Step 3: Train ML Models

**Option A - Automated Setup:**
```bash
# Run setup script (installs + trains)
python setup_unsw_system.py
```

**Option B - Manual Training:**
```bash
# Train all 3 models
python backend/ml/train_unsw_models.py
```

**Training Time:** 5-15 minutes depending on hardware

**What Gets Trained:**
1. Random Forest (100 trees, max_depth=20)
2. Logistic Regression (SAGA solver)
3. XGBoost (100 estimators, max_depth=10)

**Output:**
- `backend/ml/models/unsw_random_forest.pkl`
- `backend/ml/models/unsw_logistic_regression.pkl`
- `backend/ml/models/unsw_xgboost.pkl`
- `backend/ml/models/unsw_best_model.pkl` (best performer)
- `backend/ml/models/unsw_preprocessor.pkl` (scaler + encoders)
- `backend/ml/models/unsw_model_metadata.pkl` (metrics)

### Step 4: Configure Environment

Edit `.env` file:

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/siem_db

# Email Alerts (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL=security-team@company.com
```

---

## 🚀 Running the System

### Method 1: Batch Files (Windows)

```bash
# Step 1: Setup (first time only)
1_SETUP_UNSW_SYSTEM.bat

# Step 2: Start backend
2_START_UNSW_BACKEND.bat

# Step 3: Start frontend (separate terminal)
cd frontend
npm start
```

### Method 2: Manual Commands

**Terminal 1 - Backend:**
```bash
venv\Scripts\activate
uvicorn backend.api.main_unsw:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Access Points

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Root**: http://localhost:8000

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    UNSW-NB15 Dataset                    │
│         (Training Set + Testing Set CSV Files)          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              ML Training Pipeline                        │
│  • Data Preprocessing (UNSWDatasetLoader)               │
│  • Feature Engineering (49 features)                    │
│  • SMOTE Class Balancing                                │
│  • Train 3 Models (RF, LR, XGBoost)                     │
│  • Model Evaluation & Selection                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Real-Time Streaming Service                    │
│  • Load Test Dataset                                     │
│  • Stream Events (1-2 sec intervals)                    │
│  • ML Prediction per Event                              │
│  • Risk Score Calculation                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend                             │
│  • Process Alerts                                        │
│  • Store in MongoDB                                      │
│  • WebSocket Broadcasting                                │
│  • IP Blocking Logic                                     │
│  • Email Notifications                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              React Dashboard                             │
│  • Live Alert Feed                                       │
│  • Statistics & Charts                                   │
│  • Attack Distribution                                   │
│  • Top Source IPs                                        │
│  • System Status                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔬 ML Model Details

### Features Used (49 total)

**Network Flow Features:**
- Source/Dest ports, Protocol, State, Service
- Duration, Bytes sent/received, TTL values
- Packet counts, Window sizes, TCP base sequence
- Mean packet sizes, Transaction depth

**Behavioral Features:**
- Load rates (Sload, Dload)
- Jitter (Sjit, Djit)
- Inter-packet times (Sintpkt, Dintpkt)
- TCP round-trip time, SYN-ACK, ACK-DAT

**Connection Features:**
- State TTL, Flow HTTP method
- FTP login attempts, FTP commands
- Service connections (source/dest)
- Destination/Source lifetime metrics

### Attack Categories

| Category | Severity | Description |
|----------|----------|-------------|
| **Exploit** | HIGH | Exploitation of vulnerabilities |
| **DoS** | HIGH | Denial of Service attacks |
| **Backdoor** | HIGH | Backdoor installation |
| **Shellcode** | HIGH | Shellcode execution |
| **Worm** | HIGH | Worm propagation |
| **Reconnaissance** | MEDIUM | Network scanning/probing |
| **Analysis** | MEDIUM | Traffic analysis |
| **Fuzzer** | MEDIUM | Fuzzing attacks |
| **Generic** | MEDIUM | Generic attack patterns |
| **Normal** | LOW | Legitimate traffic |

### Model Performance

Typical results after training:

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| **Random Forest** | 92-95% | 90-93% | 88-92% | 89-92% |
| **XGBoost** | 91-94% | 89-92% | 87-91% | 88-91% |
| **Logistic Regression** | 85-88% | 83-86% | 82-85% | 82-85% |

---

## 📡 API Endpoints

### Alerts

```http
GET /alerts?limit=100&severity=HIGH
```
Get recent alerts with optional filtering

```http
GET /alerts/stats
```
Get alert statistics (total, by severity, distribution)

```http
GET /alerts/timeline?hours=24
```
Get hourly alert timeline

### Security

```http
GET /security/blocked-ips
```
Get list of blocked IP addresses

### System

```http
GET /system/status
```
Get system status and streaming info

```http
GET /models/info
```
Get ML model metadata and performance

### WebSocket

```
ws://localhost:8000/ws
```
Real-time alert streaming

**Message Types:**
- `alert` - New detection alert
- `statistics` - Updated statistics
- `ip_blocked` - IP blocked notification
- `heartbeat` - Keep-alive ping
- `connected` - Connection established

---

## 🎨 Dashboard Features

### Live Threat Feed
- Real-time scrolling alerts
- Color-coded severity (RED/YELLOW/GREEN)
- Attack type icons
- Risk scores (0-100)
- ML confidence percentages
- Source/Dest IP, ports, protocol
- Risk indicators list

### Statistics Cards
1. **Total Detections** - All-time alert count
2. **Critical Threats** - HIGH severity count
3. **Moderate Threats** - MEDIUM severity count
4. **Minor Issues** - LOW severity count
5. **Blocked IPs** - Quarantined addresses
6. **Live Connections** - Active WebSocket clients

### Widgets
- **Attack Distribution** - Top 10 attack types
- **Top Source IPs** - Most active attackers with risk scores
- **Blocked IPs** - Quarantined addresses with reasons
- **System Status** - Model info, streaming progress

### Notifications
- Browser notifications for HIGH alerts
- Sound alerts for critical threats
- Visual pulse animation when live

---

## 🔧 Configuration Options

### Streaming Interval

Edit `backend/runtime/unsw_stream_service.py`:

```python
self.stream_interval = 1.5  # seconds between events
```

### IP Blocking Threshold

Edit `backend/api/main_unsw.py`:

```python
if high_count >= 2:  # Block after 2 HIGH violations
```

### Email Alert Threshold

Edit `backend/api/main_unsw.py`:

```python
if alert['risk_score'] > 70:  # Send email if risk > 70
```

### Risk Score Calculation

Edit `backend/runtime/unsw_stream_service.py`:

```python
severity_multipliers = {
    'Exploit': 1.3,
    'DoS': 1.3,
    'Backdoor': 1.4,
    # ... customize multipliers
}
```

---

## 🐛 Troubleshooting

### Dataset Not Found
```
❌ Dataset not found: backend/datasets/UNSW_NB15_training-set.csv
```
**Solution:** Download dataset files and place in `backend/datasets/`

### Model Not Loaded
```
❌ Failed to load model: [Errno 2] No such file or directory
```
**Solution:** Run training first: `python backend/ml/train_unsw_models.py`

### MongoDB Connection Failed
```
❌ MongoDB connection failed
```
**Solution:** Check `.env` file has correct `MONGODB_URI`

### WebSocket 403 Forbidden
```
INFO: connection rejected (403 Forbidden)
```
**Solution:** Make sure you're running `main_unsw.py` not old API files

### No Alerts Appearing
**Check:**
1. Backend logs show "Started UNSW-NB15 streaming"
2. Test dataset loaded successfully
3. WebSocket shows "LIVE" in dashboard
4. Browser console shows no errors

---

## 📈 Performance Optimization

### For Faster Training
- Reduce `n_estimators` in models (100 → 50)
- Reduce `max_depth` (20 → 10)
- Use smaller training sample

### For Faster Streaming
- Increase `stream_interval` (1.5 → 3.0 seconds)
- Reduce alert history limit (100 → 50)

### For Lower Memory Usage
- Limit MongoDB query results
- Clear old alerts periodically
- Reduce WebSocket broadcast frequency

---

## 🎓 Understanding the Output

### Alert Example

```json
{
  "timestamp": "2024-02-21T10:30:45.123Z",
  "event_type": "intrusion_detection",
  "threat_type": "exploit",
  "severity": "HIGH",
  "risk_score": 87.5,
  "message": "High confidence Exploit detected from 192.168.1.100",
  "source_ip": "192.168.1.100",
  "dest_ip": "10.0.0.50",
  "source_port": 54321,
  "dest_port": 80,
  "protocol": "tcp",
  "ml_confidence": 0.92,
  "ml_prediction": 1,
  "detected_by": "UNSW-NB15 ML Model",
  "detection_method": "machine_learning",
  "attack_category": "Exploit",
  "risk_factors": [
    "High ML confidence: 92.0%",
    "Attack type: Exploit",
    "High packet count"
  ]
}
```

### Risk Score Calculation

```
Base Score = ML Confidence × 100
Multiplied by Attack Severity (1.1 - 1.4)
Capped at 100
```

**Example:**
- ML Confidence: 0.85 (85%)
- Attack Type: DoS (multiplier 1.3)
- Risk Score: 85 × 1.3 = 110.5 → capped at 100

---

## 🔐 Security Best Practices

1. **Change Default Credentials** - Update MongoDB and email passwords
2. **Use HTTPS** - Enable SSL/TLS in production
3. **Restrict CORS** - Limit allowed origins in production
4. **Rate Limiting** - Add API rate limits
5. **Authentication** - Add user authentication for dashboard
6. **Firewall Rules** - Restrict backend port access
7. **Regular Updates** - Keep dependencies updated

---

## 📚 Additional Resources

- **UNSW-NB15 Dataset**: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **XGBoost**: https://xgboost.readthedocs.io/
- **Scikit-learn**: https://scikit-learn.org/

---

## 🎉 Success Indicators

Your system is working correctly when you see:

✅ Backend logs: "Started UNSW-NB15 streaming"  
✅ Dashboard shows "LIVE" with pulsing indicator  
✅ Alerts appearing every 1-2 seconds  
✅ Statistics updating in real-time  
✅ Model info banner showing accuracy  
✅ No console errors in browser  
✅ WebSocket connection stable  

---

## 📞 Support

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review backend logs for errors
3. Check browser console (F12) for frontend errors
4. Verify all files are in correct locations
5. Ensure dataset files are downloaded

---

**Built with ❤️ using UNSW-NB15 Dataset, FastAPI, React, and Machine Learning**
