# 🛡️ Mini SIEM - AI-Powered Security Risk Detection System

A comprehensive, enterprise-level Security Information and Event Management (SIEM) system built with AI/ML capabilities for real-time threat detection and monitoring.

---

# 🎯 Project Overview

This Mini SIEM system provides:

- Real-time threat detection using Machine Learning
- Dynamic risk scoring with human-readable alerts
- WebSocket-based live updates to dashboard
- Automated IP blocking for repeat offenders
- Email notifications for high-severity threats
- Multi-threat detection: Phishing, Brute Force, DoS, Malware, Network Probing

---

# 🏗️ Architecture

## Backend (Python / FastAPI)

- **FastAPI** – High-performance async API framework  
- **MongoDB Atlas** – Cloud database for alert storage  
- **Scikit-learn** – Machine Learning models  
- **WebSocket** – Real-time bidirectional communication  
- **SMTP** – Email notification system  

## Frontend (React)

- **React** – Modern UI framework  
- **WebSocket Client** – Real-time alert streaming  
- **Dark SOC Theme** – Professional security operations center interface  

---

# 🤖 ML Models

1. **Phishing Detection**
   - TF-IDF + Random Forest / Logistic Regression

2. **Login Anomaly Detection**
   - Random Forest / Isolation Forest

3. **Network Traffic Classification**
   - Multi-class classification (Normal / DoS / Probe / Brute Force)

4. **Malware Detection**
   - Random Forest classifier

---

# 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- MongoDB Atlas Account
- Gmail Account (for email notifications)

