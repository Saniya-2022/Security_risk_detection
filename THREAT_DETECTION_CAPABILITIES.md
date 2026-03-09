# WHAT THE RISK DETECTION SYSTEM IDENTIFIES
## Security Risk Detection with Human Readable Alerts

---

## 🎯 OVERVIEW

The system identifies **4 major categories** of security threats using **4 specialized ML models** with **80-95% accuracy**.

---

## 1️⃣ EMAIL THREATS (Phishing Detection)

### Detection Method:
- **ML Model:** Logistic Regression / Random Forest
- **Technology:** TF-IDF Vectorization + Scikit-learn
- **Accuracy:** 80-95%

### What It Identifies:

| Threat Type | Detection Criteria | Risk Score |
|-------------|-------------------|------------|
| **Phishing Emails** | Suspicious sender domains (.tk, .ml, .ga, .cf) | 30-100 |
| **Suspicious Links** | 3+ links in email body | 35 points |
| **Phishing Keywords** | 3+ keywords (urgent, verify, suspended, prize) | 30 points |
| **Malicious Attachments** | .exe, .scr, .bat, .vbs, .js files | 70 points |
| **Double Extensions** | file.pdf.exe (disguised files) | 20 points |
| **Legitimate Emails** | Normal business emails | 0 points |

### Examples Detected:
✅ "URGENT: Verify your account immediately" from security@paypal-verify.ml  
✅ "Your account has been suspended" with multiple links  
✅ "You've won a prize!" with suspicious attachments  
✅ Invoice.exe attachments  
❌ "Monthly Newsletter" from newsletter@company.com (Safe)

### Alert Output:
```
HIGH Risk: Suspicious phishing email detected from security@paypal-verify.ml

Threat Indicators:
• Multiple phishing keywords detected
• Multiple suspicious links in email
• ML model high confidence threat detection

Recommended Action:
• Do not click any links or download attachments
• Report to security team immediately
• Block sender domain
```

---

## 2️⃣ LOGIN THREATS (Brute Force & Anomaly Detection)

### Detection Method:
- **ML Model:** Random Forest / Isolation Forest
- **Technology:** Behavioral Analysis + Scikit-learn
- **Accuracy:** 80-95%

### What It Identifies:

| Threat Type | Detection Criteria | Risk Score |
|-------------|-------------------|------------|
| **Brute Force Attacks** | 10+ failed login attempts | 60 points |
| **Multiple Failed Logins** | 5-9 failed attempts | 40 points |
| **Suspicious Countries** | Login from RU, CN, KP, IR | 20 points |
| **Unusual Time Login** | Login at 0-5 AM (late night) | 15 points |
| **High Login Frequency** | 50+ login attempts per minute | 40 points |
| **Normal Login** | 0-2 failed attempts, business hours | 0 points |

### Examples Detected:
✅ 15 failed login attempts from 203.0.113.50 (Russia) at 2 AM  
✅ Rapid login attempts (100+ per minute)  
✅ Login from suspicious country with multiple failures  
❌ Successful login from US during business hours (Safe)

### Alert Output:
```
HIGH Risk: Multiple failed login attempts detected from IP 203.0.113.50

Threat Indicators:
• Excessive failed login attempts - possible brute force
• Login from suspicious country
• ML model high confidence threat detection

Recommended Action:
• Block source IP address immediately
• Lock affected user account
• Enable MFA if not already active
```

---

## 3️⃣ NETWORK THREATS (Traffic Classification)

### Detection Method:
- **ML Model:** Logistic Regression / Random Forest
- **Technology:** Multi-class Classification + Scikit-learn
- **Accuracy:** 80-95%

### What It Identifies:

| Threat Type | Detection Criteria | Risk Score |
|-------------|-------------------|------------|
| **DoS Attack** | 500+ requests per minute | 80 points |
| **High Request Rate** | 100-499 requests per minute | 50 points |
| **Port Scanning (Probe)** | Random port access, 100-300 requests | 45 points |
| **Brute Force (Network)** | 50-150 requests to SSH/FTP/RDP ports | 40 points |
| **Suspicious Ports** | Access to ports 22, 21, 3389, random ports | 30 points |
| **Normal Traffic** | 1-50 requests, standard ports (80, 443) | 0 points |

### Attack Classifications:
1. **DoS (Denial of Service)** - Overwhelming server with requests
2. **Probe** - Port scanning and reconnaissance
3. **BruteForce** - Network-level brute force attempts
4. **Normal** - Legitimate traffic

### Examples Detected:
✅ 1500 requests/min from 45.33.32.156 to port 80 (DoS)  
✅ Sequential port scanning from 198.51.100.25 (Probe)  
✅ 100 connection attempts to SSH port 22 (BruteForce)  
❌ 10 HTTPS requests to port 443 (Normal)

### Alert Output:
```
HIGH Risk: Possible DoS attack detected due to excessive requests from IP 45.33.32.156

Threat Indicators:
• Possible DoS attack pattern
• ML model high confidence threat detection

Recommended Action:
• Activate DDoS mitigation
• Block attacking IP ranges
• Scale infrastructure if needed
```

---

## 4️⃣ MALWARE THREATS (File Scanning)

### Detection Method:
- **ML Model:** Random Forest Classifier
- **Technology:** Feature-based Classification + Scikit-learn
- **Accuracy:** 80-95%

### What It Identifies:

| Threat Type | Detection Criteria | Risk Score |
|-------------|-------------------|------------|
| **Malware Files** | .exe, .bat, .scr, .vbs, .js extensions | 50-100 |
| **Suspicious Scripts** | Encoded patterns, obfuscation | 40 points |
| **Large Executables** | 10KB-5MB executable files | Variable |
| **Encoded Patterns** | 5+ encoded/obfuscated sections | 30 points |
| **Safe Files** | .pdf, .docx, .txt, .jpg, .png | 0 points |

### File Types Analyzed:
**Dangerous:**
- .exe (Executable)
- .bat (Batch script)
- .scr (Screen saver - often malware)
- .vbs (Visual Basic script)
- .js (JavaScript - can be malicious)

**Safe:**
- .pdf (Documents)
- .docx (Word documents)
- .txt (Text files)
- .jpg, .png (Images)

### Examples Detected:
✅ file_1234.exe with 15 encoded patterns (Malware)  
✅ script.vbs with suspicious script indicators  
✅ document.scr disguised as document  
❌ report.pdf with 0 encoded patterns (Safe)

### Alert Output:
```
HIGH Risk: Potentially malicious file detected: file_1234.exe

Threat Indicators:
• ML model high confidence threat detection

Recommended Action:
• Quarantine file immediately
• Run full system scan
• Isolate affected system
```

---

## 🎯 FUTURE MALWARE DETECTION (Planned)

### Advanced Malware Types to be Added:

| Malware Type | Description | Detection Method |
|--------------|-------------|------------------|
| **Trojan Horse** | Hidden malicious code in legitimate software | Behavioral analysis + Signature |
| **Logic Bomb** | Time/condition-triggered malicious code | Code pattern analysis |
| **Ransomware** | File encryption malware | File access pattern + Encryption detection |
| **Masquerade Attack** | Impersonation/identity spoofing | Behavioral biometrics |
| **Virus** | Self-replicating malicious code | Signature scanning + Heuristics |
| **Worm** | Self-propagating malware | Network behavior analysis |
| **Rootkit** | Privilege escalation malware | System integrity checks |
| **Spyware** | Data theft malware | Network traffic analysis |

---

## 📊 RISK SCORING SYSTEM

### How Risk Scores are Calculated:

```
Risk Score = Sum of all detected threat indicators (capped at 100)

Examples:
- Phishing email (30) + Suspicious links (35) + ML confidence (50) = 100 (HIGH)
- Failed logins (40) + Suspicious country (20) = 60 (MEDIUM)
- High request rate (50) = 50 (MEDIUM)
- Normal activity = 0 (LOW)
```

### Severity Classification:

| Risk Score | Severity | Color | Action |
|------------|----------|-------|--------|
| **71-100** | HIGH | 🔴 Red | Immediate action required |
| **31-70** | MEDIUM | 🟡 Yellow | Monitor and investigate |
| **0-30** | LOW | 🟢 Green | Log for reference |

---

## 🔍 DETECTION METHODS

### 1. Machine Learning Detection
- 4 trained models (Logistic Regression, Random Forest, Isolation Forest)
- TF-IDF text vectorization for emails
- Feature engineering for behavioral analysis
- 80-95% accuracy across all models

### 2. Rule-Based Detection
- Pattern matching for known threats
- Threshold-based triggers
- Signature detection
- Behavioral rules

### 3. Anomaly Detection
- Isolation Forest algorithm
- Behavioral baseline comparison
- Statistical outlier detection
- Deviation from normal patterns

### 4. Correlation Engine (Enterprise)
- Multi-event pattern detection
- Time-based correlation
- Source-based correlation
- Attack chain identification

---

## 🌍 THREAT INTELLIGENCE INTEGRATION

### Geographic Detection:
- **Suspicious Countries:** Russia (RU), China (CN), North Korea (KP), Iran (IR)
- **Safe Countries:** US, UK, Canada (CA), Germany (DE), France (FR)
- **GeoIP Mapping:** Automatic country detection from IP addresses

### MITRE ATT&CK Mapping:
The system maps detected threats to 20+ MITRE ATT&CK techniques:

| Threat Type | MITRE Technique |
|-------------|-----------------|
| Phishing | T1566 - Phishing |
| Brute Force | T1110 - Brute Force |
| DoS | T1498 - Network DoS |
| Port Scanning | T1046 - Network Service Scanning |
| Malware | T1204 - User Execution |

---

## 🚨 AUTOMATED RESPONSE ACTIONS

### What Happens When Threats are Detected:

**HIGH Severity (Risk Score 71-100):**
1. ✅ Alert saved to MongoDB database
2. ✅ Real-time WebSocket broadcast to dashboard
3. ✅ Email notification sent to security team
4. ✅ IP address automatically blocked (for network threats)
5. ✅ Violation recorded in IP blocker database
6. ✅ Human-readable alert generated

**MEDIUM Severity (Risk Score 31-70):**
1. ✅ Alert saved to database
2. ✅ Dashboard notification
3. ✅ Logged for monitoring
4. ⚠️ No automatic blocking (requires review)

**LOW Severity (Risk Score 0-30):**
1. ✅ Alert saved to database
2. ✅ Dashboard display
3. ℹ️ Informational only

---

## 📈 DETECTION STATISTICS

### Event Generation:
- **Frequency:** Every 3-7 seconds (randomized)
- **Event Types:** Login (35%), Network (35%), Email (20%), Malware (10%)
- **Threat Probability:** 
  - Login: 30% suspicious
  - Network: 25% attacks
  - Email: 35% phishing
  - Malware: 20% malicious

### Detection Performance:
- **Processing Time:** <100ms per event
- **ML Inference:** <100ms per prediction
- **Alert Generation:** Real-time (instant)
- **Database Write:** <10ms
- **WebSocket Broadcast:** <50ms latency

---

## 🎯 REAL-WORLD THREAT EXAMPLES

### Example 1: Phishing Attack
```
Event: Email received from security@paypal-verify.ml
Subject: "URGENT: Verify your account immediately"
Body: Contains 5 suspicious links
Attachment: invoice.exe

Detection:
✅ ML Model: 89% phishing probability
✅ Suspicious sender domain (.ml)
✅ Phishing keywords detected
✅ Malicious attachment (.exe)

Result:
Risk Score: 100/100 (HIGH)
Action: Email blocked, sender domain flagged
```

### Example 2: Brute Force Attack
```
Event: 18 failed login attempts from 203.0.113.50
Username: admin
Country: Russia (RU)
Time: 2:30 AM

Detection:
✅ ML Model: 94% anomaly probability
✅ Excessive failed attempts
✅ Suspicious country
✅ Unusual time

Result:
Risk Score: 100/100 (HIGH)
Action: IP blocked automatically, account locked
```

### Example 3: DoS Attack
```
Event: 1,847 requests per minute from 45.33.32.156
Port: 80 (HTTP)
Duration: 5 minutes
Protocol: TCP

Detection:
✅ ML Model: 96% DoS probability
✅ Extreme request rate
✅ Attack pattern detected

Result:
Risk Score: 80/100 (HIGH)
Action: IP blocked, DDoS mitigation activated
```

### Example 4: Malware Detection
```
Event: File scan of "document.exe"
Extension: .exe
Size: 2.5 MB
Encoded patterns: 12
Suspicious scripts: Yes

Detection:
✅ ML Model: 91% malware probability
✅ Executable file type
✅ Multiple encoded patterns
✅ Suspicious script indicators

Result:
Risk Score: 100/100 (HIGH)
Action: File quarantined, system scan initiated
```

---

## ✅ SUMMARY: WHAT THE SYSTEM IDENTIFIES

### Current Detection Capabilities:

**1. Email Threats:**
- ✅ Phishing emails
- ✅ Suspicious links
- ✅ Malicious attachments
- ✅ Spoofed senders

**2. Login Threats:**
- ✅ Brute force attacks
- ✅ Failed login attempts
- ✅ Suspicious geographic locations
- ✅ Unusual time access

**3. Network Threats:**
- ✅ DoS attacks
- ✅ Port scanning (Probe)
- ✅ Network brute force
- ✅ Suspicious traffic patterns

**4. Malware Threats:**
- ✅ Malicious executables
- ✅ Suspicious scripts
- ✅ Encoded/obfuscated files
- ✅ Dangerous file types

**5. Automated Actions:**
- ✅ IP blocking
- ✅ Email notifications
- ✅ Real-time alerts
- ✅ Risk scoring
- ✅ Human-readable explanations

### Future Enhancements:
- 🚧 Trojan Horse detection
- 🚧 Logic Bomb identification
- 🚧 Ransomware detection
- 🚧 Masquerade attack detection
- 🚧 Virus scanning
- 🚧 Mobile push notifications
- 🚧 Hardware buzzer alerts
- 🚧 IoT sensor integration

---

**Total Threat Types Detected:** 15+ current, 25+ planned  
**Detection Accuracy:** 80-95%  
**Response Time:** Real-time (<1 second)  
**Automated Actions:** 5 types  
**Alert Formats:** Human-readable plain English
