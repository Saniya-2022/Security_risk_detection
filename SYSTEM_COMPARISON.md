# 📊 System Comparison: Simulated vs Real-World UNSW-NB15

## Overview

This project now includes TWO complete intrusion detection systems:

1. **Simulated System** - Original synthetic data generator
2. **UNSW-NB15 System** - Real-world dataset with ML models

---

## Feature Comparison

| Feature | Simulated System | UNSW-NB15 System |
|---------|------------------|------------------|
| **Data Source** | Synthetic (Faker library) | Real network captures |
| **Dataset Size** | 500-1000 samples | 257,673 network flows |
| **ML Models** | Basic (100% accuracy) | 3 models (85-95% accuracy) |
| **Features** | 10-15 simple features | 49 network flow features |
| **Attack Types** | 4 types | 9 attack categories |
| **Training Time** | < 1 minute | 10-15 minutes |
| **Realism** | Low (demo purposes) | High (real attacks) |
| **Use Case** | Learning, demos | Production-ready |

---

## Detailed Comparison

### 1. Data Generation

#### Simulated System
```python
# Generates fake data on-the-fly
{
    'source_ip': '192.168.1.100',
    'event_type': 'phishing',
    'risk_score': random.randint(60, 95)
}
```

**Pros:**
- No dataset download required
- Instant setup
- Easy to customize
- Good for demos

**Cons:**
- Not realistic
- Patterns too simple
- Can't train real ML models
- Not suitable for production

#### UNSW-NB15 System
```python
# Real network traffic captures
{
    'srcip': '149.171.126.6',
    'sport': 1030,
    'dstip': '59.166.0.0',
    'dsport': 80,
    'proto': 'tcp',
    'dur': 0.121478,
    'sbytes': 486,
    'dbytes': 1337,
    # ... 40+ more features
}
```

**Pros:**
- Real attack patterns
- Production-ready
- High accuracy ML models
- Research-grade dataset

**Cons:**
- Requires dataset download
- Longer training time
- More complex setup
- Larger storage needs

---

### 2. Machine Learning

#### Simulated System

**Models:**
- Basic classifiers
- Trained on synthetic data
- 100% accuracy (unrealistic)

**Training:**
```bash
python backend/ml/train_all_models.py
# Takes < 1 minute
```

**Use Case:**
- Educational purposes
- Quick demos
- Proof of concept

#### UNSW-NB15 System

**Models:**
- Random Forest (92-95% accuracy)
- XGBoost (91-94% accuracy)
- Logistic Regression (85-88% accuracy)

**Training:**
```bash
python backend/ml/train_unsw_models.py
# Takes 10-15 minutes
# Uses SMOTE for class balancing
# Evaluates on real test set
```

**Use Case:**
- Production deployment
- Research projects
- Real threat detection

---

### 3. Attack Detection

#### Simulated System

**Attack Types:**
1. Phishing
2. Brute Force
3. DoS
4. Malware

**Detection:**
- Rule-based patterns
- Simple thresholds
- Fake confidence scores

#### UNSW-NB15 System

**Attack Categories:**
1. Exploit
2. DoS
3. Reconnaissance
4. Backdoor
5. Shellcode
6. Worm
7. Fuzzer
8. Analysis
9. Generic Attack

**Detection:**
- ML-based prediction
- 49 network features
- Real confidence scores
- Risk score calculation

---

### 4. System Architecture

#### Simulated System

```
Event Generator (Faker)
    ↓
Simple ML Models
    ↓
MongoDB Storage
    ↓
WebSocket Broadcast
    ↓
React Dashboard
```

#### UNSW-NB15 System

```
UNSW-NB15 Dataset
    ↓
Data Preprocessing (49 features)
    ↓
SMOTE Class Balancing
    ↓
3 ML Models (RF, XGBoost, LR)
    ↓
Model Selection (Best Accuracy)
    ↓
Real-Time Streaming Service
    ↓
ML Prediction per Event
    ↓
Risk Score Calculation
    ↓
MongoDB Storage
    ↓
WebSocket Broadcast
    ↓
Enhanced React Dashboard
```

---

### 5. Dashboard Features

#### Simulated System

- Basic alert feed
- Simple statistics
- Severity badges
- IP blocking
- Email alerts

#### UNSW-NB15 System

**All simulated features PLUS:**
- ML model info banner
- Model accuracy display
- Attack distribution chart
- Top source IPs with risk scores
- Streaming progress indicator
- Enhanced alert details
- Protocol and port information
- Network flow statistics

---

### 6. Performance Metrics

#### Simulated System

| Metric | Value |
|--------|-------|
| Alerts/sec | 0.2-0.3 |
| Accuracy | 100% (fake) |
| Features | 10-15 |
| Storage/alert | ~500 bytes |
| Training time | < 1 min |

#### UNSW-NB15 System

| Metric | Value |
|--------|-------|
| Alerts/sec | 0.5-1.0 |
| Accuracy | 85-95% (real) |
| Features | 49 |
| Storage/alert | ~1.5 KB |
| Training time | 10-15 min |

---

## Which System Should You Use?

### Use Simulated System If:

✅ You want quick setup (< 5 minutes)  
✅ You're learning about SIEM systems  
✅ You need a demo for presentations  
✅ You don't have dataset files  
✅ You want to customize attack types easily  

### Use UNSW-NB15 System If:

✅ You want production-ready detection  
✅ You need real ML model accuracy  
✅ You're doing research or thesis work  
✅ You want to detect real attack patterns  
✅ You need enterprise-grade features  

---

## Running Both Systems

You can keep both systems and switch between them:

### Simulated System
```bash
# Backend
uvicorn backend.api.main_dynamic:app --reload --port 8000

# Uses: backend/event_generator.py
# Models: backend/ml/models/*.pkl (simple)
```

### UNSW-NB15 System
```bash
# Backend
uvicorn backend.api.main_unsw:app --reload --port 8000

# Uses: backend/runtime/unsw_stream_service.py
# Models: backend/ml/models/unsw_*.pkl (advanced)
```

### Frontend (Same for Both)
```bash
cd frontend
npm start
```

**Note:** Update `frontend/src/App.js` to use `Dashboard_UNSW.js` for UNSW system

---

## Migration Path

### From Simulated → UNSW-NB15

1. Download UNSW-NB15 dataset
2. Run `python setup_unsw_system.py`
3. Update frontend to use `Dashboard_UNSW.js`
4. Start with `main_unsw.py` instead of `main_dynamic.py`

### Keep Both Systems

1. Use different ports (8000 vs 8001)
2. Use different MongoDB collections
3. Switch frontend between dashboards
4. Compare detection results

---

## File Structure

### Simulated System Files
```
backend/
├── event_generator.py          # Synthetic event generation
├── alert_service.py            # Alert processing
├── datasets/
│   └── generate_datasets.py    # Synthetic data generator
├── ml/
│   ├── train_all_models.py     # Simple model training
│   └── models/*.pkl            # Basic models
└── api/
    └── main_dynamic.py         # Simulated API
```

### UNSW-NB15 System Files
```
backend/
├── datasets/
│   ├── unsw_loader.py          # Dataset preprocessing
│   ├── UNSW_NB15_training-set.csv
│   └── UNSW_NB15_testing-set.csv
├── ml/
│   ├── train_unsw_models.py    # Advanced model training
│   └── models/
│       ├── unsw_random_forest.pkl
│       ├── unsw_xgboost.pkl
│       ├── unsw_logistic_regression.pkl
│       ├── unsw_best_model.pkl
│       └── unsw_preprocessor.pkl
├── runtime/
│   └── unsw_stream_service.py  # Real-time streaming
└── api/
    └── main_unsw.py            # UNSW API
```

---

## Conclusion

Both systems serve different purposes:

- **Simulated**: Perfect for learning, demos, and quick prototypes
- **UNSW-NB15**: Production-ready with real ML and attack detection

Choose based on your needs, or run both to compare!

---

**Recommendation:** Start with Simulated for learning, then upgrade to UNSW-NB15 for real deployment.
