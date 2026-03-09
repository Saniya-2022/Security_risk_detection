# 🛡️ Mini SIEM - AI-Powered Security Risk Detection System

A comprehensive, enterprise-level Security Information and Event Management (SIEM) system built with AI/ML capabilities for real-time threat detection and monitoring.

## 🎯 Project Overview

This Mini SIEM system provides:
- **Real-time threat detection** using Machine Learning
- **Dynamic risk scoring** with human-readable alerts
- **WebSocket-based live updates** to dashboard
- **Automated IP blocking** for repeat offenders
- **Email notifications** for high-severity threats
- **Multi-threat detection**: Phishing, Brute Force, DoS, Malware, Network Probing

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **FastAPI** - High-performance async API framework
- **MongoDB Atlas** - Cloud database for alert storage
- **Scikit-learn** - Machine Learning models
- **WebSocket** - Real-time bidirectional communication
- **SMTP** - Email notification system

### Frontend (React)
- **React** - Modern UI framework
- **WebSocket Client** - Real-time alert streaming
- **Dark SOC Theme** - Professional security operations center interface

### ML Models
1. **Phishing Detection** - TF-IDF + Random Forest/Logistic Regression
2. **Login Anomaly** - Random Forest/Isolation Forest
3. **Network Traffic Classification** - Multi-class classification (Normal/DoS/Probe/BruteForce)
4. **Malware Detection** - Random Forest classifier

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- MongoDB Atlas account
- Gmail account (for email notifications)

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd mini-siem
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables
Create a `.env` file in the root directory:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/security_risk_detection
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

**Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

### 3. Generate Datasets
```bash
python backend/datasets/generate_datasets.py
```

This creates:
- `backend/datasets/email_dataset.csv` (500 samples)
- `backend/datasets/login_dataset.csv` (500 samples)
- `backend/datasets/network_dataset.csv` (1000 samples)
- `backend/datasets/malware_dataset.csv` (500 samples)

### 4. Train ML Models
```bash
python backend/ml/train_all_models.py
```

This trains and saves:
- `backend/ml/models/phishing_model.pkl`
- `backend/ml/models/login_model.pkl`
- `backend/ml/models/network_model.pkl`
- `backend/ml/models/malware_model.pkl`

### 5. Start Backend Server
```bash
# Using the enhanced API
uvicorn backend.api.main_enhanced:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`
Swagger docs at: `http://localhost:8000/docs`

### 6. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Dashboard will open at: `http://localhost:3000`

## 📡 API Endpoints

### Detection Endpoints
- `POST /detect/phishing` - Detect phishing emails
- `POST /detect/login` - Detect login anomalies
- `POST /detect/network` - Classify network traffic
- `POST /detect/malware` - Detect malware files

### Alert Management
- `GET /alerts` - Get all alerts (with limit)
- `GET /alerts/severity/{severity}` - Filter by severity
- `GET /alerts/stats` - Get alert statistics

### Security Management
- `GET /security/blocked-ips` - List blocked IPs
- `POST /security/block-ip` - Manually block IP
- `POST /security/unblock-ip` - Unblock IP

### System
- `GET /system/status` - System health status
- `WS /ws` - WebSocket connection for real-time updates

## 🧪 Testing the System

### Test Phishing Detection
```bash
curl -X POST "http://localhost:8000/detect/phishing" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "urgent@secure-bank.tk",
    "subject": "URGENT: Verify your account",
    "body": "Click here to verify your account immediately",
    "num_links": 5,
    "suspicious_keywords": 4
  }'
```

### Test Login Anomaly
```bash
curl -X POST "http://localhost:8000/detect/login" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "192.168.1.100",
    "username": "admin",
    "failed_attempts": 10,
    "time_of_login": 3,
    "country": "RU",
    "login_frequency": 150
  }'
```

### Test Network Traffic
```bash
curl -X POST "http://localhost:8000/detect/network" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "10.0.0.50",
    "request_count_per_min": 800,
    "port_number": 80,
    "packet_size": 50,
    "protocol": "TCP",
    "duration": 5
  }'
```

### Test Malware Detection
```bash
curl -X POST "http://localhost:8000/detect/malware" \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "suspicious.exe",
    "extension": "exe",
    "file_size": 500000,
    "encoded_patterns": 15,
    "suspicious_script": 1
  }'
```

## 🎨 Dashboard Features

### Real-Time Monitoring
- Live alert feed with WebSocket updates
- Color-coded severity indicators (RED/YELLOW/GREEN)
- Threat type icons and classifications
- ML confidence scores

### Statistics
- Total alerts counter
- Severity distribution (HIGH/MEDIUM/LOW)
- Blocked IP count
- Active WebSocket connections

### Threat Analysis
- Threat type distribution chart
- Risk factor breakdown
- Human-readable explanations
- Recommended actions

### IP Management
- Blocked IP list with reasons
- Block timestamps
- Automatic blocking on repeated violations

## 🔒 Security Features

### Dynamic Risk Scoring
- Failed login attempts: +40-60 points
- High request rate: +50-80 points
- Phishing keywords: +30 points
- ML high confidence: +50-70 points

### Risk Levels
- **0-30**: LOW (Green)
- **31-70**: MEDIUM (Yellow)
- **71-100**: HIGH (Red)

### Automated Response
- HIGH alerts trigger email notifications
- 2+ HIGH violations = automatic IP block
- Real-time dashboard updates
- Audit trail in MongoDB

## 📊 ML Model Performance

Models are trained with comparison between algorithms:

| Model | Algorithm Options | Typical Accuracy |
|-------|------------------|------------------|
| Phishing | Logistic Regression / Random Forest | 85-95% |
| Login Anomaly | Random Forest / Isolation Forest | 80-90% |
| Network Traffic | Logistic Regression / Random Forest | 85-92% |
| Malware | Random Forest | 88-95% |

## 🗄️ MongoDB Schema

### Alerts Collection
```javascript
{
  "_id": ObjectId,
  "threat_type": "phishing|brute_force|dos|probe|malware",
  "risk_score": 0-100,
  "severity": "LOW|MEDIUM|HIGH",
  "ml_probability": 0.0-1.0,
  "is_threat": boolean,
  "details": {...},
  "risk_factors": [...],
  "human_readable_alert": "...",
  "timestamp": ISODate
}
```

### Blocked IPs Collection
```javascript
{
  "_id": ObjectId,
  "ip_address": "x.x.x.x",
  "reason": "...",
  "blocked_at": ISODate,
  "last_blocked": ISODate,
  "block_count": number,
  "status": "blocked|unblocked"
}
```

### IP Violations Collection
```javascript
{
  "_id": ObjectId,
  "ip_address": "x.x.x.x",
  "threat_type": "...",
  "risk_score": number,
  "details": {...},
  "timestamp": ISODate
}
```

## 🎓 Academic Use

This project is designed for academic demonstration of:
- AI/ML in cybersecurity
- Real-time threat detection systems
- SIEM architecture and design
- Full-stack development with security focus
- WebSocket real-time communication
- Dynamic risk assessment algorithms

## 📝 Project Structure

```
mini-siem/
├── backend/
│   ├── api/
│   │   ├── main_enhanced.py       # Enhanced FastAPI app
│   │   └── websocket_manager.py   # WebSocket handler
│   ├── datasets/
│   │   └── generate_datasets.py   # Dataset generator
│   ├── detection/
│   │   ├── phishing_detector.py
│   │   ├── malware_detector.py
│   │   └── ...
│   ├── ml/
│   │   ├── train_all_models.py    # ML training pipeline
│   │   ├── ml_service.py          # ML prediction service
│   │   └── models/                # Trained models
│   ├── security/
│   │   └── ip_blocker.py          # IP blocking logic
│   ├── database/
│   │   └── mongo.py               # MongoDB connection
│   ├── runtime/
│   │   └── email_service.py       # Email notifications
│   └── risk_engine.py             # Risk scoring engine
├── frontend/
│   ├── src/
│   │   ├── Dashboard.js           # Main dashboard
│   │   ├── Dashboard.css          # SOC theme styling
│   │   └── App.js
│   └── package.json
├── requirements.txt
├── .env
└── README.md
```

## 🔧 Troubleshooting

### MongoDB Connection Issues
- Verify MONGO_URI in `.env`
- Check MongoDB Atlas network access (whitelist your IP)
- Ensure database user has read/write permissions

### Email Notifications Not Working
- Use Gmail App Password, not regular password
- Enable "Less secure app access" if needed
- Check SENDER_EMAIL and SENDER_PASSWORD in `.env`

### WebSocket Connection Failed
- Ensure backend is running on port 8000
- Check CORS settings in main_enhanced.py
- Verify frontend is connecting to correct WebSocket URL

### ML Models Not Loading
- Run `python backend/ml/train_all_models.py` first
- Check that `backend/ml/models/` directory exists
- Verify all dataset CSV files are generated

## 📧 Contact & Support

For questions or issues:
- Email: sreeja.warangal834@gmail.com
- Check API docs: http://localhost:8000/docs

## 📄 License

This project is for academic purposes. Please cite appropriately if used in research or publications.

---

**Built with ❤️ for Cybersecurity Education**
