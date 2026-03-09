# 📚 Mini SIEM - Complete Project Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Component Details](#component-details)
3. [API Documentation](#api-documentation)
4. [Database Schema](#database-schema)
5. [ML Models](#ml-models)
6. [Risk Scoring Algorithm](#risk-scoring-algorithm)
7. [WebSocket Protocol](#websocket-protocol)
8. [Deployment Guide](#deployment-guide)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  React Dashboard (Port 3000)                         │  │
│  │  - Real-time WebSocket connection                    │  │
│  │  - Alert visualization                               │  │
│  │  - Statistics & charts                               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                      Backend Layer (FastAPI)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Endpoints (Port 8000)                           │  │
│  │  - Detection endpoints                               │  │
│  │  - Alert management                                  │  │
│  │  - WebSocket handler                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ML Service Layer                                    │  │
│  │  - Phishing detection                                │  │
│  │  - Login anomaly detection                           │  │
│  │  - Network traffic classification                    │  │
│  │  - Malware detection                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Risk Engine                                         │  │
│  │  - Dynamic risk scoring                              │  │
│  │  - Severity classification                           │  │
│  │  - Human-readable alert generation                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Security Layer                                      │  │
│  │  - IP blocking mechanism                             │  │
│  │  - Violation tracking                                │  │
│  │  - Automated response                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MongoDB Atlas                                       │  │
│  │  - alerts collection                                 │  │
│  │  - blocked_ips collection                            │  │
│  │  - ip_violations collection                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Backend Components

#### A. API Layer (`backend/api/`)
- **main_enhanced.py**: Main FastAPI application with all endpoints
- **websocket_manager.py**: WebSocket connection manager for real-time updates

#### B. ML Service (`backend/ml/`)
- **ml_service.py**: Unified ML prediction service
- **train_all_models.py**: Complete training pipeline
- **models/**: Directory containing trained models

#### C. Detection Engines (`backend/detection/`)
- **phishing_detector.py**: Email phishing detection
- **malware_detector.py**: Malware file detection
- **email_detector.py**: Email attachment analysis
- **parser.py**: Log parsing utilities

#### D. Risk Engine (`backend/risk_engine.py`)
- Dynamic risk scoring
- Severity classification
- Human-readable alert generation
- Recommended action logic

#### E. Security Layer (`backend/security/`)
- **ip_blocker.py**: IP blocking and violation tracking

#### F. Database Layer (`backend/database/`)
- **mongo.py**: MongoDB connection and operations

#### G. Runtime Services (`backend/runtime/`)
- **email_service.py**: SMTP email notifications
- **runtime_engine.py**: Real-time monitoring engine

### 2. Frontend Components

#### A. Dashboard (`frontend/src/Dashboard.js`)
- Real-time alert feed
- WebSocket connection management
- Statistics visualization
- Blocked IP management
- System status monitoring

#### B. Styling (`frontend/src/Dashboard.css`)
- Dark SOC theme
- Responsive design
- Color-coded severity indicators
- Animations and transitions

---

## API Documentation

### Detection Endpoints

#### 1. Phishing Detection
```http
POST /detect/phishing
Content-Type: application/json

{
  "sender": "string",
  "subject": "string",
  "body": "string",
  "attachment": "string",
  "num_links": 0,
  "suspicious_keywords": 0
}
```

**Response:**
```json
{
  "threat_type": "phishing",
  "risk_score": 85,
  "severity": "HIGH",
  "ml_probability": 0.92,
  "is_threat": true,
  "details": {...},
  "risk_factors": ["Multiple phishing keywords detected", ...],
  "human_readable_alert": "HIGH Risk: Suspicious phishing email detected...",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 2. Login Anomaly Detection
```http
POST /detect/login
Content-Type: application/json

{
  "ip_address": "string",
  "username": "string",
  "failed_attempts": 0,
  "time_of_login": 12,
  "country": "US",
  "login_frequency": 1
}
```

#### 3. Network Traffic Classification
```http
POST /detect/network
Content-Type: application/json

{
  "ip_address": "string",
  "request_count_per_min": 100,
  "port_number": 80,
  "packet_size": 1000,
  "protocol": "TCP",
  "duration": 10
}
```

#### 4. Malware Detection
```http
POST /detect/malware
Content-Type: application/json

{
  "file_name": "string",
  "extension": "string",
  "file_size": 1000,
  "encoded_patterns": 0,
  "suspicious_script": 0
}
```

### Alert Management Endpoints

#### Get All Alerts
```http
GET /alerts?limit=100
```

#### Get Alerts by Severity
```http
GET /alerts/severity/{severity}
```
Parameters: `severity` = LOW | MEDIUM | HIGH

#### Get Alert Statistics
```http
GET /alerts/stats
```

**Response:**
```json
{
  "total_alerts": 150,
  "by_severity": {
    "HIGH": 25,
    "MEDIUM": 50,
    "LOW": 75
  },
  "threat_distribution": [
    {"_id": "phishing", "count": 40},
    {"_id": "brute_force", "count": 30},
    ...
  ]
}
```

### Security Management Endpoints

#### Get Blocked IPs
```http
GET /security/blocked-ips
```

#### Block IP Address
```http
POST /security/block-ip?ip_address=x.x.x.x&reason=Manual+block
```

#### Unblock IP Address
```http
POST /security/unblock-ip?ip_address=x.x.x.x
```

### System Endpoints

#### System Status
```http
GET /system/status
```

#### WebSocket Connection
```
WS /ws
```

---

## Database Schema

### Collections

#### 1. alerts
```javascript
{
  _id: ObjectId,
  threat_type: String,           // "phishing", "brute_force", "dos", "probe", "malware"
  risk_score: Number,            // 0-100
  severity: String,              // "LOW", "MEDIUM", "HIGH"
  ml_probability: Number,        // 0.0-1.0
  is_threat: Boolean,
  details: Object,               // Threat-specific details
  risk_factors: Array<String>,   // List of risk indicators
  human_readable_alert: String,  // Human-readable description
  timestamp: Date
}
```

#### 2. blocked_ips
```javascript
{
  _id: ObjectId,
  ip_address: String,
  reason: String,
  blocked_at: Date,
  last_blocked: Date,
  block_count: Number,
  status: String                 // "blocked", "unblocked"
}
```

#### 3. ip_violations
```javascript
{
  _id: ObjectId,
  ip_address: String,
  threat_type: String,
  risk_score: Number,
  details: Object,
  timestamp: Date
}
```

---

## ML Models

### 1. Phishing Detection Model

**Algorithm**: Random Forest / Logistic Regression (best selected)

**Features**:
- TF-IDF vectorized text (subject + body + sender)
- Number of links
- Suspicious keyword count

**Training Data**: 500 samples (50% phishing, 50% legitimate)

**Performance**: ~85-95% accuracy

### 2. Login Anomaly Detection Model

**Algorithm**: Random Forest / Isolation Forest (best selected)

**Features**:
- Failed login attempts
- Time of login (hour)
- Login frequency
- Country code (encoded)

**Training Data**: 500 samples (50% normal, 50% brute force)

**Performance**: ~80-90% accuracy

### 3. Network Traffic Classification Model

**Algorithm**: Random Forest / Logistic Regression (best selected)

**Features**:
- Request count per minute
- Port number
- Packet size
- Protocol (encoded)
- Duration

**Classes**: Normal, DoS, Probe, BruteForce

**Training Data**: 1000 samples

**Performance**: ~85-92% accuracy

### 4. Malware Detection Model

**Algorithm**: Random Forest

**Features**:
- File extension (encoded)
- File size
- Encoded pattern count
- Suspicious script presence

**Training Data**: 500 samples (50% safe, 50% malware)

**Performance**: ~88-95% accuracy

---

## Risk Scoring Algorithm

### Scoring Rules

| Factor | Threshold | Score | Description |
|--------|-----------|-------|-------------|
| Failed Login Attempts | ≥5 | +40 | Multiple failed attempts |
| Failed Login Attempts | ≥10 | +60 | Excessive failed attempts |
| Request Rate | ≥100/min | +50 | High request rate |
| Request Rate | ≥500/min | +80 | DoS pattern |
| Phishing Keywords | ≥3 | +30 | Multiple suspicious keywords |
| Suspicious Links | ≥3 | +35 | Multiple links in email |
| ML Confidence | ≥0.7 | +50 | High confidence detection |
| ML Confidence | ≥0.9 | +70 | Critical confidence detection |

### Severity Classification

- **LOW** (0-30): Minimal risk, monitoring only
- **MEDIUM** (31-70): Moderate risk, investigation recommended
- **HIGH** (71-100): Critical risk, immediate action required

### Automated Actions

- **HIGH severity**: 
  - Email notification sent
  - Logged for analysis
  - Broadcast via WebSocket

- **2+ HIGH violations from same IP**:
  - Automatic IP blocking
  - Block notification broadcast
  - Audit trail created

---

## WebSocket Protocol

### Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

### Message Types

#### 1. Alert Message
```json
{
  "type": "alert",
  "data": {
    "threat_type": "phishing",
    "risk_score": 85,
    "severity": "HIGH",
    ...
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 2. IP Block Notification
```json
{
  "type": "ip_blocked",
  "data": {
    "ip_address": "x.x.x.x",
    "reason": "Multiple HIGH severity violations",
    "blocked_at": "2024-01-01T12:00:00"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 3. Heartbeat
```json
{
  "type": "heartbeat",
  "message": "connected",
  "timestamp": "2024-01-01T12:00:00"
}
```

---

## Deployment Guide

### Production Deployment

#### 1. Environment Setup
```bash
# Create production .env
MONGO_URI=mongodb+srv://prod-user:password@cluster.mongodb.net/siem_prod
SENDER_EMAIL=alerts@company.com
SENDER_PASSWORD=app-password
```

#### 2. Backend Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Generate datasets and train models
python backend/datasets/generate_datasets.py
python backend/ml/train_all_models.py

# Run with Gunicorn (production)
gunicorn backend.api.main_enhanced:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 3. Frontend Deployment
```bash
cd frontend
npm install
npm run build

# Serve with nginx or deploy to hosting service
```

#### 4. Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend/build;
        try_files $uri /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Docker Deployment (Optional)

#### Dockerfile (Backend)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ ./backend/
COPY .env .

CMD ["uvicorn", "backend.api.main_enhanced:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGO_URI=${MONGO_URI}
      - SENDER_EMAIL=${SENDER_EMAIL}
      - SENDER_PASSWORD=${SENDER_PASSWORD}
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

---

## Performance Optimization

### Backend Optimization
1. Use connection pooling for MongoDB
2. Implement caching for frequent queries
3. Use async operations for I/O-bound tasks
4. Load ML models once at startup

### Frontend Optimization
1. Implement virtual scrolling for large alert lists
2. Debounce WebSocket message handling
3. Use React.memo for expensive components
4. Lazy load dashboard widgets

### Database Optimization
1. Create indexes on frequently queried fields
2. Implement TTL indexes for old alerts
3. Use aggregation pipelines for statistics
4. Archive old data periodically

---

## Security Considerations

1. **API Security**:
   - Implement rate limiting
   - Add authentication/authorization
   - Use HTTPS in production
   - Validate all inputs

2. **Database Security**:
   - Use strong credentials
   - Enable MongoDB authentication
   - Restrict network access
   - Regular backups

3. **Email Security**:
   - Use app-specific passwords
   - Implement email rate limiting
   - Validate recipient addresses

4. **WebSocket Security**:
   - Implement authentication
   - Use WSS (WebSocket Secure)
   - Validate message origins

---

## Monitoring & Maintenance

### Health Checks
- Monitor API response times
- Track WebSocket connection count
- Monitor database performance
- Check ML model accuracy

### Logging
- Log all security events
- Track API usage
- Monitor error rates
- Audit IP blocking actions

### Maintenance Tasks
- Retrain ML models monthly
- Archive old alerts
- Review blocked IPs
- Update threat signatures

---

**Last Updated**: 2024
**Version**: 2.0.0
