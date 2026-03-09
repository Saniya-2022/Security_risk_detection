"""
Enhanced FastAPI Main Application for Mini SIEM
Complete API with WebSocket, ML detection, and real-time monitoring
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel

# Detection Engines
from backend.detection.phishing_detector import detect_phishing
from backend.detection.malware_detector import detect_malware

# ML Services
from backend.ml.ml_service import (
    predict_phishing_ml,
    predict_login_anomaly,
    predict_network_traffic,
    predict_malware
)

# Risk Engine
from backend.risk_engine import (
    calculate_dynamic_risk,
    generate_human_readable_alert,
    classify_severity
)

# Database
from backend.database.mongo import db, alerts_collection

# Security
from backend.security.ip_blocker import (
    record_ip_violation,
    is_ip_blocked,
    get_blocked_ips,
    unblock_ip,
    block_ip
)

# WebSocket
from backend.api.websocket_manager import manager

# Email Service
from backend.runtime.email_service import send_alert_email


# ============================================
# FASTAPI APP INITIALIZATION
# ============================================

app = FastAPI(
    title="Mini SIEM - Security Risk Detection API",
    description="AI-powered real-time security monitoring system",
    version="2.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# PYDANTIC MODELS
# ============================================

class EmailData(BaseModel):
    sender: str
    subject: str
    body: str
    attachment: str = ""
    num_links: int = 0
    suspicious_keywords: int = 0


class LoginData(BaseModel):
    ip_address: str
    username: str
    failed_attempts: int = 0
    time_of_login: int = 12
    country: str = "US"
    login_frequency: int = 1


class NetworkTrafficData(BaseModel):
    ip_address: str
    request_count_per_min: int
    port_number: int
    packet_size: int
    protocol: str = "TCP"
    duration: int = 10


class FileData(BaseModel):
    file_name: str
    extension: str
    file_size: int
    encoded_patterns: int = 0
    suspicious_script: int = 0


# ============================================
# HELPER FUNCTIONS
# ============================================

def serialize_alert(alert):
    """Convert MongoDB ObjectId to string"""
    alert["_id"] = str(alert["_id"])
    return alert


async def save_and_broadcast_alert(alert_data: Dict[str, Any]):
    """Save alert to database and broadcast via WebSocket"""
    
    # Save to MongoDB
    result = alerts_collection.insert_one(alert_data)
    alert_data["_id"] = str(result.inserted_id)
    
    # Broadcast to WebSocket clients
    await manager.broadcast_alert(alert_data)
    
    # Send email if HIGH severity
    if alert_data["severity"] == "HIGH":
        try:
            email_body = f"""
🚨 HIGH SEVERITY SECURITY ALERT

Threat Type: {alert_data.get('threat_type', 'Unknown')}
Risk Score: {alert_data['risk_score']}/100
Severity: {alert_data['severity']}

{alert_data.get('human_readable_alert', '')}

Timestamp: {alert_data['timestamp']}
"""
            send_alert_email(
                receiver_email="sreeja.warangal834@gmail.com",
                subject=f"🚨 HIGH ALERT: {alert_data.get('threat_type', 'Security Threat')}",
                body=email_body
            )
        except Exception as e:
            print(f"Email notification failed: {e}")
    
    return alert_data


# ============================================
# ROOT ENDPOINT
# ============================================

@app.get("/")
def home():
    return {
        "message": "Mini SIEM API v2.0 - Real-Time Security Monitoring",
        "status": "operational",
        "features": [
            "AI-powered threat detection",
            "Real-time WebSocket alerts",
            "Dynamic risk scoring",
            "IP blocking mechanism",
            "Email notifications"
        ]
    }


# ============================================
# WEBSOCKET ENDPOINT
# ============================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time alert streaming"""
    
    await manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive and receive messages
            data = await websocket.receive_text()
            
            # Echo back for heartbeat
            await websocket.send_json({
                "type": "heartbeat",
                "message": "connected",
                "timestamp": datetime.utcnow().isoformat()
            })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ============================================
# ALERT ENDPOINTS
# ============================================

@app.get("/alerts")
async def get_all_alerts(limit: int = 100):
    """Get all alerts with optional limit"""
    
    alerts = alerts_collection.find().sort("timestamp", -1).limit(limit)
    return [serialize_alert(alert) for alert in alerts]


@app.get("/alerts/severity/{severity}")
async def get_alerts_by_severity(severity: str):
    """Get alerts filtered by severity"""
    
    alerts = alerts_collection.find({"severity": severity.upper()}).sort("timestamp", -1)
    return [serialize_alert(alert) for alert in alerts]


@app.get("/alerts/stats")
async def get_alert_statistics():
    """Get alert statistics"""
    
    total = alerts_collection.count_documents({})
    high = alerts_collection.count_documents({"severity": "HIGH"})
    medium = alerts_collection.count_documents({"severity": "MEDIUM"})
    low = alerts_collection.count_documents({"severity": "LOW"})
    
    # Get threat type distribution
    pipeline = [
        {"$group": {"_id": "$threat_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    threat_distribution = list(alerts_collection.aggregate(pipeline))
    
    return {
        "total_alerts": total,
        "by_severity": {
            "HIGH": high,
            "MEDIUM": medium,
            "LOW": low
        },
        "threat_distribution": threat_distribution
    }


# ============================================
# EMAIL PHISHING DETECTION
# ============================================

@app.post("/detect/phishing")
async def detect_phishing_email(email_data: EmailData):
    """Detect phishing in email using ML + rules"""
    
    email_dict = email_data.dict()
    
    # ML Prediction
    ml_result = predict_phishing_ml(email_dict)
    
    # Calculate dynamic risk
    detection_data = {
        "suspicious_keywords": email_dict.get("suspicious_keywords", 0),
        "num_links": email_dict.get("num_links", 0),
        "ml_probability": ml_result["probability"]
    }
    
    risk_result = calculate_dynamic_risk(detection_data)
    
    # Generate human-readable alert
    human_alert = generate_human_readable_alert(
        threat_type="phishing",
        risk_score=risk_result["risk_score"],
        severity=risk_result["severity"],
        details={"sender": email_dict["sender"], "subject": email_dict["subject"]},
        risk_factors=risk_result["risk_factors"]
    )
    
    # Create alert document
    alert_data = {
        "threat_type": "phishing",
        "risk_score": risk_result["risk_score"],
        "severity": risk_result["severity"],
        "ml_probability": ml_result["probability"],
        "is_threat": ml_result["is_phishing"],
        "details": email_dict,
        "risk_factors": risk_result["risk_factors"],
        "human_readable_alert": human_alert,
        "timestamp": datetime.utcnow()
    }
    
    # Save and broadcast
    await save_and_broadcast_alert(alert_data)
    
    return alert_data


# ============================================
# LOGIN ANOMALY DETECTION
# ============================================

@app.post("/detect/login")
async def detect_login_anomaly(login_data: LoginData):
    """Detect login anomalies and brute force attacks"""
    
    login_dict = login_data.dict()
    
    # Check if IP is blocked
    if is_ip_blocked(login_dict["ip_address"]):
        raise HTTPException(status_code=403, detail="IP address is blocked")
    
    # ML Prediction
    ml_result = predict_login_anomaly(login_dict)
    
    # Calculate dynamic risk
    detection_data = {
        "failed_attempts": login_dict.get("failed_attempts", 0),
        "ml_probability": ml_result["probability"]
    }
    
    risk_result = calculate_dynamic_risk(detection_data)
    
    # Generate human-readable alert
    human_alert = generate_human_readable_alert(
        threat_type="brute_force",
        risk_score=risk_result["risk_score"],
        severity=risk_result["severity"],
        details={"ip_address": login_dict["ip_address"], "username": login_dict["username"]},
        risk_factors=risk_result["risk_factors"]
    )
    
    # Create alert document
    alert_data = {
        "threat_type": "brute_force",
        "risk_score": risk_result["risk_score"],
        "severity": risk_result["severity"],
        "ml_probability": ml_result["probability"],
        "is_threat": ml_result["is_anomaly"],
        "details": login_dict,
        "risk_factors": risk_result["risk_factors"],
        "human_readable_alert": human_alert,
        "timestamp": datetime.utcnow()
    }
    
    # Record violation and check for blocking
    if risk_result["severity"] == "HIGH":
        record_ip_violation(
            login_dict["ip_address"],
            "brute_force",
            risk_result["risk_score"],
            login_dict
        )
    
    # Save and broadcast
    await save_and_broadcast_alert(alert_data)
    
    return alert_data


# ============================================
# NETWORK TRAFFIC CLASSIFICATION
# ============================================

@app.post("/detect/network")
async def detect_network_threat(traffic_data: NetworkTrafficData):
    """Classify network traffic and detect attacks"""
    
    traffic_dict = traffic_data.dict()
    
    # Check if IP is blocked
    if is_ip_blocked(traffic_dict["ip_address"]):
        raise HTTPException(status_code=403, detail="IP address is blocked")
    
    # ML Prediction
    ml_result = predict_network_traffic(traffic_dict)
    
    # Calculate dynamic risk
    detection_data = {
        "request_count": traffic_dict.get("request_count_per_min", 0),
        "ml_probability": ml_result["probability"]
    }
    
    risk_result = calculate_dynamic_risk(detection_data)
    
    # Map attack type to threat type
    threat_type_map = {
        "DoS": "dos",
        "Probe": "probe",
        "BruteForce": "brute_force",
        "Normal": "normal"
    }
    threat_type = threat_type_map.get(ml_result["attack_type"], "unknown")
    
    # Generate human-readable alert
    human_alert = generate_human_readable_alert(
        threat_type=threat_type,
        risk_score=risk_result["risk_score"],
        severity=risk_result["severity"],
        details={"ip_address": traffic_dict["ip_address"]},
        risk_factors=risk_result["risk_factors"]
    )
    
    # Create alert document
    alert_data = {
        "threat_type": threat_type,
        "attack_classification": ml_result["attack_type"],
        "risk_score": risk_result["risk_score"],
        "severity": risk_result["severity"],
        "ml_probability": ml_result["probability"],
        "is_threat": ml_result["attack_type"] != "Normal",
        "details": traffic_dict,
        "risk_factors": risk_result["risk_factors"],
        "human_readable_alert": human_alert,
        "timestamp": datetime.utcnow()
    }
    
    # Record violation for HIGH severity
    if risk_result["severity"] == "HIGH":
        record_ip_violation(
            traffic_dict["ip_address"],
            threat_type,
            risk_result["risk_score"],
            traffic_dict
        )
    
    # Save and broadcast
    await save_and_broadcast_alert(alert_data)
    
    return alert_data


# ============================================
# MALWARE DETECTION
# ============================================

@app.post("/detect/malware")
async def detect_malware_file(file_data: FileData):
    """Detect malware in files"""
    
    file_dict = file_data.dict()
    
    # ML Prediction
    ml_result = predict_malware(file_dict)
    
    # Calculate dynamic risk
    detection_data = {
        "ml_probability": ml_result["probability"]
    }
    
    risk_result = calculate_dynamic_risk(detection_data)
    
    # Generate human-readable alert
    human_alert = generate_human_readable_alert(
        threat_type="malware",
        risk_score=risk_result["risk_score"],
        severity=risk_result["severity"],
        details={"file_name": file_dict["file_name"]},
        risk_factors=risk_result["risk_factors"]
    )
    
    # Create alert document
    alert_data = {
        "threat_type": "malware",
        "risk_score": risk_result["risk_score"],
        "severity": risk_result["severity"],
        "ml_probability": ml_result["probability"],
        "is_threat": ml_result["is_malware"],
        "details": file_dict,
        "risk_factors": risk_result["risk_factors"],
        "human_readable_alert": human_alert,
        "timestamp": datetime.utcnow()
    }
    
    # Save and broadcast
    await save_and_broadcast_alert(alert_data)
    
    return alert_data


# ============================================
# IP BLOCKING ENDPOINTS
# ============================================

@app.get("/security/blocked-ips")
async def get_blocked_ip_list():
    """Get list of all blocked IPs"""
    return get_blocked_ips()


@app.post("/security/block-ip")
async def block_ip_address(ip_address: str, reason: str = "Manual block"):
    """Manually block an IP address"""
    
    block_ip(ip_address, reason)
    
    # Broadcast block notification
    await manager.broadcast_ip_block(ip_address, reason)
    
    return {"message": f"IP {ip_address} blocked successfully", "ip_address": ip_address}


@app.post("/security/unblock-ip")
async def unblock_ip_address(ip_address: str):
    """Unblock an IP address"""
    
    unblock_ip(ip_address)
    
    return {"message": f"IP {ip_address} unblocked successfully", "ip_address": ip_address}


# ============================================
# SYSTEM STATUS
# ============================================

@app.get("/system/status")
async def get_system_status():
    """Get overall system status"""
    
    total_alerts = alerts_collection.count_documents({})
    high_alerts = alerts_collection.count_documents({"severity": "HIGH"})
    blocked_ips_count = len(get_blocked_ips())
    
    status = {
        "status": "operational",
        "total_alerts": total_alerts,
        "high_severity_alerts": high_alerts,
        "blocked_ips": blocked_ips_count,
        "active_websocket_connections": len(manager.active_connections),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
