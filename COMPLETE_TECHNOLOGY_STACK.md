# TECHNOLOGY STACK
## Security Risk Detection with Human Readable Alerts

---

## 1️⃣ FRONTEND

### Core Framework
- **React.js 19.2.4** – Interactive dashboard UI with component-based architecture
- **HTML5, CSS3, JavaScript** – Structure, styling, and client-side logic
- **React DOM** – Rendering engine for web browsers

### Visualization & Charts
- **Chart.js 4.5.1** – Real-time graphs & analytics visualization
- **react-chartjs-2 5.3.1** – React wrapper for Chart.js integration
- **Dynamic Charts** – Live updating threat distribution, timeline graphs

### Real-Time Communication
- **WebSocket** – Bidirectional real-time alert streaming
- **Live Updates** – Continuous dashboard refresh without page reload
- **Event-Driven UI** – Instant alert notifications

### Additional Frontend Features
- **Responsive Design** – Mobile-friendly interface
- **Real-Time Clock** – Live timestamp display
- **Color-Coded Alerts** – Visual severity indicators (Red/Yellow/Green)

---

## 2️⃣ BACKEND

### Core Framework
- **FastAPI (Python 3.12)** – High-performance async REST API framework
- **Uvicorn** – ASGI server for running FastAPI applications
- **Asyncio** – Asynchronous I/O for concurrent operations

### Real-Time Communication
- **WebSockets** – Real-time alert broadcasting to connected clients
- **WebSocket Manager** – Connection pooling and message distribution
- **Heartbeat Mechanism** – Connection health monitoring

### Data Validation & Modeling
- **Pydantic** – Data validation & schema modeling
- **Type Hints** – Strong typing for Python code
- **Request/Response Models** – Structured API contracts

### Event Processing
- **Event Generator** – Continuous security event simulation (3-7 sec intervals)
- **Alert Service** – Event processing and alert generation pipeline
- **Async Task Queue** – Background job processing

---

## 3️⃣ MACHINE LEARNING & DETECTION

### ML Framework
- **Scikit-learn** – Machine learning library for threat detection
- **NumPy** – Numerical computing for feature engineering
- **Pandas** – Data manipulation and preprocessing
- **Joblib** – Model serialization and loading

### ML Models (4 Trained Models)
1. **Email Phishing Detection**
   - Algorithm: Logistic Regression / Random Forest
   - Features: TF-IDF vectorization, link count, suspicious keywords
   - Accuracy: 80-95%

2. **Login Anomaly Detection**
   - Algorithm: Random Forest / Isolation Forest
   - Features: Failed attempts, login time, frequency, geolocation
   - Accuracy: 80-95%

3. **Network Traffic Classification**
   - Algorithm: Logistic Regression / Random Forest
   - Classes: Normal, DoS, Probe, BruteForce
   - Accuracy: 80-95%

4. **Malware Detection**
   - Algorithm: Random Forest
   - Features: File extension, size, encoded patterns, suspicious scripts
   - Accuracy: 80-95%

### Detection Engines
- **Rule-Based Detection Engine** – Pattern matching for known threats
- **Custom Risk Scoring Algorithm** – Multi-factor risk calculation (0-100)
- **Anomaly Detection** – Isolation Forest for behavioral analysis
- **Correlation Engine** – Multi-event pattern detection

### Advanced Malware Detection (Future Enhancement)
- **Trojan Horse Detection** – Hidden malicious code identification
- **Logic Bomb Detection** – Time/condition-based threat detection
- **Ransomware Detection** – File encryption pattern analysis
- **Masquerade Attack Detection** – Identity spoofing identification
- **Virus Scanning** – Signature-based malware detection
- **Behavioral Analysis** – Runtime behavior monitoring

---

## 4️⃣ DATABASE

### Primary Database
- **MongoDB** – NoSQL document database for alert storage & logs
- **PyMongo 4.5.0** – Synchronous MongoDB driver
- **Motor 3.3.2** – Asynchronous MongoDB driver (for enterprise features)
- **MongoDB Atlas** – Cloud-hosted database service

### Database Features
- **Flexible Schema** – Dynamic alert structure support
- **Indexing** – Fast query performance on timestamps and severity
- **Aggregation Pipeline** – Real-time statistics calculation
- **Time-Series Data** – Efficient alert timeline storage

### Data Models
- **Alert Model** – Complete alert information with metadata
- **Incident Model** – Correlated security incidents
- **Email Model** – Email-specific threat data

---

## 5️⃣ SECURITY & THREAT INTELLIGENCE

### Authentication & Authorization
- **JWT Authentication** – Secure API access (Future Enhancement)
- **Token-Based Auth** – Stateless authentication mechanism
- **Role-Based Access Control** – User permission management

### Threat Intelligence
- **MITRE ATT&CK Mapping** – 20+ threat technique classifications
- **GeoIP Location Detection** – Country-based threat analysis
- **Threat Enrichment Service** – External threat intelligence integration
- **CVE Database Integration** – Vulnerability information lookup

### Security Features
- **Automatic IP Blocking** – Real-time threat response
- **IP Blocker Service** – Persistent blocked IP management
- **Rate Limiting** – API abuse prevention
- **CORS Configuration** – Cross-origin security

### API Documentation
- **Swagger UI (OpenAPI)** – Interactive API testing & documentation
- **FastAPI Auto-Docs** – Automatic API schema generation
- **Endpoint Documentation** – Comprehensive API reference

---

## 6️⃣ NOTIFICATION & ALERTING SYSTEM

### Current Implementation
- **Email Notifications** – SMTP-based email alerts for HIGH severity
- **WebSocket Alerts** – Real-time dashboard notifications
- **In-App Notifications** – Browser-based alert display

### Future Enhancements
- **Mobile Push Notifications** – SMS and app-based alerts
- **Twilio Integration** – SMS notification service
- **Firebase Cloud Messaging** – Mobile app push notifications
- **Multi-Channel Alerts** – Email + SMS + Push simultaneously

### IoT & Hardware Integration (Future)
- **Buzzer/Sound Alerts** – Physical audio alerts for critical threats
- **Raspberry Pi Integration** – Hardware sensor connectivity
- **Arduino Support** – Microcontroller-based alert system
- **LED Indicators** – Visual hardware alert signals
- **GPIO Control** – Physical device triggering

---

## 7️⃣ MONITORING & ANALYTICS

### Real-Time Monitoring
- **Live Dashboard** – Continuous data streaming
- **WebSocket Heartbeat** – Connection health monitoring
- **System Health Checks** – Database and service status monitoring
- **Active Connection Tracking** – WebSocket client management

### Analytics & Reporting
- **Threat Distribution Analysis** – Attack type breakdown
- **Timeline Visualization** – Historical alert patterns
- **Risk Score Trends** – Severity analysis over time
- **Geographic Threat Mapping** – Location-based threat visualization

### Performance Monitoring
- **Event Generation Rate** – 3-7 second intervals
- **Alert Processing Time** – Real-time latency tracking
- **Database Query Performance** – MongoDB operation metrics
- **WebSocket Throughput** – Message delivery statistics

---

## 8️⃣ DEVELOPMENT & DEPLOYMENT

### Development Tools
- **Git** – Version control system
- **npm** – Frontend package manager
- **pip** – Python package manager
- **Virtual Environment (venv)** – Python dependency isolation

### Code Quality
- **ESLint** – JavaScript code linting
- **Python Logging** – Application-level logging
- **Error Handling** – Comprehensive exception management
- **Type Checking** – Python type hints validation

### Testing
- **Jest** – JavaScript testing framework
- **React Testing Library** – Component testing
- **pytest** – Python testing framework (Future)
- **API Testing** – Swagger UI interactive testing

### Deployment
- **Uvicorn Server** – Production ASGI server
- **Port Configuration** – Backend (8000), Frontend (3000)
- **Environment Variables** – Configuration management (.env)
- **CORS Setup** – Cross-origin resource sharing

---

## 9️⃣ DATA PROCESSING & GENERATION

### Event Generation
- **Custom Event Generator** – Realistic security event simulation
- **Randomized Timing** – 3-7 second intervals for realism
- **Multi-Type Events** – Login, Email, Network, Malware
- **Probability Weighting** – Realistic threat distribution

### Data Processing Pipeline
- **Async Processing** – Non-blocking event handling
- **Feature Extraction** – ML model input preparation
- **Risk Calculation** – Multi-factor scoring algorithm
- **Alert Formatting** – Human-readable text generation

### Text Processing
- **TF-IDF Vectorization** – Email content analysis
- **Natural Language Generation** – Plain English alert creation
- **Keyword Extraction** – Suspicious pattern identification

---

## 🔟 SYSTEM ARCHITECTURE PATTERN

### Backend Architecture
- **Event-Driven Architecture** – Async event processing
- **Microservices-Style Design** – Modular component structure
- **RESTful API** – Standard HTTP endpoints
- **WebSocket Streaming** – Real-time data push

### Frontend Architecture
- **Single Page Application (SPA)** – No page reloads
- **Component-Based Design** – Reusable React components
- **State Management** – React hooks (useState, useEffect)
- **Real-Time Updates** – WebSocket event listeners

### Data Flow
```
Event Source → Event Generator → Detection Engine → 
Risk Scoring → Threat Intelligence → Alert Generation → 
Database Storage → WebSocket Broadcast → Dashboard Display
```

---

## 📊 TECHNOLOGY SUMMARY

| Layer | Technologies | Count |
|-------|-------------|-------|
| **Frontend** | React, Chart.js, WebSocket | 3 core |
| **Backend** | FastAPI, Uvicorn, Asyncio | 3 core |
| **ML Models** | Scikit-learn (4 models) | 4 models |
| **Database** | MongoDB, PyMongo, Motor | 1 database |
| **Intelligence** | MITRE, GeoIP, Correlation | 3 services |
| **Notifications** | Email, WebSocket, Mobile (future) | 3 channels |
| **Hardware (future)** | Raspberry Pi, Arduino, Sensors | 3 types |

---

## 🚀 FUTURE TECHNOLOGY ADDITIONS

### Planned Integrations
1. **Mobile Application** – React Native / Flutter app
2. **IoT Sensors** – Raspberry Pi + Arduino integration
3. **Advanced ML** – Deep learning models (TensorFlow/PyTorch)
4. **Blockchain** – Immutable audit logs
5. **Container Orchestration** – Docker + Kubernetes
6. **Load Balancing** – Nginx reverse proxy
7. **Caching Layer** – Redis for performance
8. **Message Queue** – RabbitMQ / Kafka for scalability

### Enhanced Detection
- **Behavioral Biometrics** – User behavior analysis
- **Network Traffic Analysis** – Deep packet inspection
- **Endpoint Detection** – Host-based monitoring
- **Cloud Security** – AWS/Azure threat detection

---

## ✅ TECHNOLOGY STACK ADVANTAGES

1. **Modern & Scalable** – Async architecture supports high concurrency
2. **Real-Time Capable** – WebSocket enables instant updates
3. **AI-Powered** – ML models provide intelligent detection
4. **User-Friendly** – React provides intuitive interface
5. **Extensible** – Modular design allows easy feature additions
6. **Cost-Effective** – Open-source technologies reduce costs
7. **Production-Ready** – Enterprise-grade frameworks
8. **Cross-Platform** – Web-based accessibility

---

**Last Updated:** February 2026  
**Version:** 2.1.0  
**Status:** Production-Ready with Future Enhancements Planned
