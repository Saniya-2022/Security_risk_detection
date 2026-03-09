# 📡 Mini SIEM - API Examples & Use Cases

## Table of Contents
1. [Phishing Detection Examples](#phishing-detection-examples)
2. [Login Anomaly Examples](#login-anomaly-examples)
3. [Network Traffic Examples](#network-traffic-examples)
4. [Malware Detection Examples](#malware-detection-examples)
5. [Alert Management Examples](#alert-management-examples)
6. [Security Management Examples](#security-management-examples)

---

## Phishing Detection Examples

### Example 1: High-Risk Phishing Email

**Request:**
```bash
curl -X POST "http://localhost:8000/detect/phishing" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "urgent@secure-bank.tk",
    "subject": "URGENT: Verify your account immediately",
    "body": "Dear customer, your account has been suspended due to suspicious activity. Click here to verify your identity: http://malicious-link.com/verify",
    "attachment": "invoice.exe",
    "num_links": 5,
    "suspicious_keywords": 6
  }'
```

**Response:**
```json
{
  "threat_type": "phishing",
  "risk_score": 95,
  "severity": "HIGH",
  "ml_probability": 0.94,
  "is_threat": true,
  "details": {
    "sender": "urgent@secure-bank.tk",
    "subject": "URGENT: Verify your account immediately",
    "body": "Dear customer, your account has been suspended...",
    "attachment": "invoice.exe",
    "num_links": 5,
    "suspicious_keywords": 6
  },
  "risk_factors": [
    "Multiple phishing keywords detected",
    "Multiple suspicious links in email",
    "ML model critical confidence threat detection"
  ],
  "human_readable_alert": "HIGH Risk: Suspicious phishing email detected from IP...",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Example 2: Legitimate Newsletter

**Request:**
```bash
curl -X POST "http://localhost:8000/detect/phishing" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "newsletter@company.com",
    "subject": "Monthly Product Updates - January 2024",
    "body": "Hello! Here are this month updates from our team. Check out our new features and improvements.",
    "attachment": "",
    "num_links": 1,
    "suspicious_keywords": 0
  }'
```

**Response:**
```json
{
  "threat_type": "phishing",
  "risk_score": 15,
  "severity": "LOW",
  "ml_probability": 0.12,
  "is_threat": false,
  "details": {...},
  "risk_factors": [],
  "human_readable_alert": "LOW Risk: Email appears legitimate...",
  "timestamp": "2024-01-15T10:31:00.000Z"
}
```

---

## Login Anomaly Examples

### Example 1: Brute Force Attack

**Request:**
```bash
curl -X POST "http://localhost:8000/detect/login" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "192.168.1.100",
    "username": "admin",
    "failed_attempts": 15,
    "time_of_login": 3,
    "country": "RU",
    "login_frequency": 200
  }'
```

**Response:**
```json
{
  "threat_type": "brute_force",
  "risk_score": 100,
  "severity": "HIGH",
  "ml_probability": 0.96,
  "is_threat": true,
  "details": {
    "ip_address": "192.168.1.100",
    "username": "admin",
    "failed_attempts": 15,
    "time_of_login": 3,
    "country": "RU",
    "login_frequency": 200
  },
  "risk_factors": [
    "Excessive failed login attempts - possible brute force",
    "ML model critical confidence threat detection"
  ],
  "human_readable_alert": "HIGH Risk: Multiple failed login attempts detected from IP 192.168.1.100.\n\nThreat Indicators:\n• Excessive failed login attempts - possible brute force\n• ML model critical confidence threat detection\n\nRecommended Action:\n• Block source IP address immediately\n• Lock affected user account\n• Enable MFA if not already active",
  "timestamp": "2024-01-15T10:32:00.000Z"
}
```

**Note**: This IP will be tracked and may be automatically blocked after 2 HIGH severity violations.

### Example 2: Normal Login

**Request:**
```bash
curl -X POST "http://localhost:8000/detect/login" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "10.0.0.50",
    "username": "john.doe",
    "failed_attempts": 0,
    "time_of_login": 14,
    "country": "US",
    "login_frequency": 5
  }'
```

**Response:**
```json
{
  "threat_type": "brute_force",
  "risk_score": 10,
  "severity": "LOW",
  "ml_probability": 0.08,
  "is_threat": false,
  "details": {...},
  "risk_factors": [],
  "human_readable_alert": "LOW Risk: Login appears normal...",
  "timestamp": "2024-01-15T10:33:00.000Z"
}
```

---

## Network Traffic Examples

### Example 1: DoS Attack

**Request:**
```bash
curl -X POST "http://localhost:8000/detect/network" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "203.0.113.50",
    "request_count_per_min": 1500,
    "port_number": 80,
    "packet_size": 50,
    "protocol": "TCP",
    "duration": 5
  }'
```

**Response:**
```json
{
  "threat_type": "dos",
  "attack_classification": "DoS",
  "risk_score": 130,
  "severity": "HIGH",
  "ml_probability": 0.98,
  "is_threat": true,
  "details": {
    "ip_address": "203.0.113.50",
    "request_count_per_min": 1500,
    "port_number": 80,
    "packet_size": 50,
    "protocol": "TCP",
    "duration": 5
  },
  "risk_factors": [
    "Possible DoS attack pattern",
    "ML model critical confidence threat detection"
  ],
  "human_readable_alert": "HIGH Risk: Possible DoS attack detected due to excessive requests from IP 203.0.113.50.\n\nThreat Indicators:\n• Possible DoS attack pattern\n• ML model critical confidence threat detection\n\nRecommended Action:\n• Activate DDoS mitigation\n• Block attacking IP ranges\n• Scale infrastructure if needed",
  "timestamp": "2024-01-15T10:34:00.000Z"
}
```

### Example 2: Port Scanning

**Request:**
```bash
curl -X POST "http://localhost:8000/detect/network" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "198.51.100.25",
    "request_count_per_min": 200,
    "port_number": 22,
    "packet_size": 100,
    "protocol": "TCP",
    "duration": 60
  }'
```

**Response:**
```json
{
  "threat_type": "probe",
  "attack_classification": "Probe",
  "risk_score": 65,
  "severity": "MEDIUM",
  "ml_probability": 0.75,
  "is_threat": true,
  "details": {...},
  "risk_factors": [
    "Abnormally high request rate detected",
    "ML model high confidence threat detection"
  ],
  "human_readable_alert": "MEDIUM Risk: Network scanning/probing activity detected...",
  "timestamp": "2024-01-15T10:35:00.000Z"
}
```

### Example 3: Normal Traffic

**Request:**
```bash
curl -X POST "http://localhost:8000/detect/network" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "192.168.1.50",
    "request_count_per_min": 20,
    "port_number": 443,
    "packet_size": 1200,
    "protocol": "HTTPS",
    "duration": 30
  }'
```

**Response:**
```json
{
  "threat_type": "normal",
  "attack_classification": "Normal",
  "risk_score": 5,
  "severity": "LOW",
  "ml_probability": 0.95,
  "is_threat": false,
  "details": {...},
  "risk_factors": [],
  "human_readable_alert": "LOW Risk: Traffic appears normal...",
  "timestamp": "2024-01-15T10:36:00.000Z"
}
```

---

## Malware Detection Examples

### Example 1: Malicious Executable

**Request:**
```bash
curl -X POST "http://localhost:8000/detect/malware" \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "invoice_payment.exe",
    "extension": "exe",
    "file_size": 500000,
    "encoded_patterns": 15,
    "suspicious_script": 1
  }'
```

**Response:**
```json
{
  "threat_type": "malware",
  "risk_score": 85,
  "severity": "HIGH",
  "ml_probability": 0.92,
  "is_threat": true,
  "details": {
    "file_name": "invoice_payment.exe",
    "extension": "exe",
    "file_size": 500000,
    "encoded_patterns": 15,
    "suspicious_script": 1
  },
  "risk_factors": [
    "ML model critical confidence threat detection"
  ],
  "human_readable_alert": "HIGH Risk: Potentially malicious file detected.\n\nThreat Indicators:\n• ML model critical confidence threat detection\n\nRecommended Action:\n• Quarantine file immediately\n• Run full system scan\n• Isolate affected system",
  "timestamp": "2024-01-15T10:37:00.000Z"
}
```

### Example 2: Safe PDF Document

**Request:**
```bash
curl -X POST "http://localhost:8000/detect/malware" \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "report_2024.pdf",
    "extension": "pdf",
    "file_size": 50000,
    "encoded_patterns": 0,
    "suspicious_script": 0
  }'
```

**Response:**
```json
{
  "threat_type": "malware",
  "risk_score": 8,
  "severity": "LOW",
  "ml_probability": 0.05,
  "is_threat": false,
  "details": {...},
  "risk_factors": [],
  "human_readable_alert": "LOW Risk: File appears safe...",
  "timestamp": "2024-01-15T10:38:00.000Z"
}
```

---

## Alert Management Examples

### Get All Alerts

**Request:**
```bash
curl -X GET "http://localhost:8000/alerts?limit=10"
```

**Response:**
```json
[
  {
    "_id": "65a5f1234567890abcdef123",
    "threat_type": "phishing",
    "risk_score": 95,
    "severity": "HIGH",
    "ml_probability": 0.94,
    "is_threat": true,
    "details": {...},
    "risk_factors": [...],
    "human_readable_alert": "...",
    "timestamp": "2024-01-15T10:30:00.000Z"
  },
  ...
]
```

### Get Alerts by Severity

**Request:**
```bash
curl -X GET "http://localhost:8000/alerts/severity/HIGH"
```

### Get Alert Statistics

**Request:**
```bash
curl -X GET "http://localhost:8000/alerts/stats"
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
    {"_id": "dos", "count": 25},
    {"_id": "probe", "count": 20},
    {"_id": "malware", "count": 15},
    {"_id": "normal", "count": 20}
  ]
}
```

---

## Security Management Examples

### Get Blocked IPs

**Request:**
```bash
curl -X GET "http://localhost:8000/security/blocked-ips"
```

**Response:**
```json
[
  {
    "ip_address": "192.168.1.100",
    "reason": "Multiple HIGH severity violations detected",
    "blocked_at": "2024-01-15T10:32:30.000Z",
    "block_count": 1
  },
  {
    "ip_address": "203.0.113.50",
    "reason": "Multiple HIGH severity violations detected",
    "blocked_at": "2024-01-15T10:34:45.000Z",
    "block_count": 2
  }
]
```

### Block IP Manually

**Request:**
```bash
curl -X POST "http://localhost:8000/security/block-ip?ip_address=10.0.0.99&reason=Manual%20security%20review"
```

**Response:**
```json
{
  "message": "IP 10.0.0.99 blocked successfully",
  "ip_address": "10.0.0.99"
}
```

### Unblock IP

**Request:**
```bash
curl -X POST "http://localhost:8000/security/unblock-ip?ip_address=10.0.0.99"
```

**Response:**
```json
{
  "message": "IP 10.0.0.99 unblocked successfully",
  "ip_address": "10.0.0.99"
}
```

---

## System Status Example

**Request:**
```bash
curl -X GET "http://localhost:8000/system/status"
```

**Response:**
```json
{
  "status": "operational",
  "total_alerts": 150,
  "high_severity_alerts": 25,
  "blocked_ips": 5,
  "active_websocket_connections": 2,
  "timestamp": "2024-01-15T10:40:00.000Z"
}
```

---

## WebSocket Example (JavaScript)

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');

// Connection opened
ws.onopen = () => {
  console.log('✅ Connected to Mini SIEM');
};

// Listen for messages
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  if (message.type === 'alert') {
    console.log('🚨 New Alert:', message.data);
    
    // Display alert in UI
    displayAlert(message.data);
    
    // Play sound for HIGH severity
    if (message.data.severity === 'HIGH') {
      playAlertSound();
    }
  } else if (message.type === 'ip_blocked') {
    console.log('🚫 IP Blocked:', message.data.ip_address);
    updateBlockedIPList();
  } else if (message.type === 'heartbeat') {
    console.log('💓 Heartbeat received');
  }
};

// Connection closed
ws.onclose = () => {
  console.log('❌ Disconnected from Mini SIEM');
  // Attempt reconnection
  setTimeout(connectWebSocket, 3000);
};

// Error handling
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

---

## Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Detect phishing
def detect_phishing(email_data):
    response = requests.post(
        f"{BASE_URL}/detect/phishing",
        json=email_data
    )
    return response.json()

# Example usage
email = {
    "sender": "urgent@secure-bank.tk",
    "subject": "URGENT: Verify your account",
    "body": "Click here immediately",
    "num_links": 5,
    "suspicious_keywords": 4
}

result = detect_phishing(email)
print(f"Risk Score: {result['risk_score']}")
print(f"Severity: {result['severity']}")
print(f"Alert: {result['human_readable_alert']}")
```

---

## Batch Testing Script

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# Test data
test_cases = [
    {
        "endpoint": "/detect/phishing",
        "data": {
            "sender": "urgent@secure-bank.tk",
            "subject": "URGENT: Verify account",
            "body": "Click here",
            "num_links": 5,
            "suspicious_keywords": 4
        }
    },
    {
        "endpoint": "/detect/login",
        "data": {
            "ip_address": "192.168.1.100",
            "username": "admin",
            "failed_attempts": 15,
            "time_of_login": 3,
            "country": "RU"
        }
    },
    # Add more test cases...
]

# Run tests
for i, test in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test['endpoint']}")
    response = requests.post(
        f"{BASE_URL}{test['endpoint']}",
        json=test['data']
    )
    result = response.json()
    print(f"  Risk Score: {result['risk_score']}")
    print(f"  Severity: {result['severity']}")
    time.sleep(1)  # Rate limiting
```

---

**For complete API documentation, visit**: http://localhost:8000/docs
