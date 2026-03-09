from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Detection Engines
from backend.detection.phishing_detector import detect_phishing
from backend.detection.malware_detector import detect_malware

# Database
from backend.database.mongo import alerts_collection

# Email Service
from backend.runtime.email_service import send_alert_email


app = FastAPI(title="Security Risk Detection API")


# -------------------------------
# CORS (Frontend Connection)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Helper: Convert Mongo ObjectId
# -------------------------------
def serialize_alert(alert):
    alert["_id"] = str(alert["_id"])
    return alert


# -------------------------------
# Root Route
# -------------------------------
@app.get("/")
def home():
    return {"message": "Security Risk Detection API Running"}


# -------------------------------
# Get All Alerts
# -------------------------------
@app.get("/alerts")
def get_all_alerts():
    alerts = alerts_collection.find().sort("created_at", -1)
    return [serialize_alert(alert) for alert in alerts]


# -------------------------------
# Phishing + Malware Detection
# -------------------------------
@app.post("/check-phishing")
def check_phishing(email_data: dict):

    # 1️⃣ Run Rule-Based Phishing Detection
    phishing_result = detect_phishing(email_data)

    # 2️⃣ Run Malware Detection
    malware_result = detect_malware(email_data)

    # 3️⃣ Choose Highest Severity Result
    result = malware_result if malware_result else phishing_result

    severity = result.get("severity", "INFO")
    risk_score = result.get("total_score", result.get("score", 0))

    # -------------------------------
    # Save Alert in MongoDB
    # -------------------------------
    alert_document = {
        "type": result.get("type", "phishing"),
        "email_data": email_data,
        "risk_score": risk_score,
        "severity": severity,
        "alert": {
            "details": result.get("details"),
            "recommended_action": result.get("recommended_action")
        },
        "created_at": datetime.utcnow()
    }

    alerts_collection.insert_one(alert_document)

    # -------------------------------
    # Send Email Notification
    # -------------------------------
    if severity in ["MEDIUM", "HIGH", "CRITICAL"]:

        details = result.get("details", [])
        recommended_action = result.get(
            "recommended_action",
            "Review immediately."
        )

        formatted_details = "\n".join(
            [f"• {item}" for item in details]
        )

        body = f"""
🚨 SECURITY ALERT NOTIFICATION

========================================
Severity Level : {severity}
Risk Score     : {risk_score}
Alert Type     : {result.get("type", "Unknown")}
========================================

📧 Email Information:
----------------------------------------
Sender     : {email_data.get("sender")}
Subject    : {email_data.get("subject")}
Attachment : {email_data.get("attachment")}

🔍 Threat Analysis:
----------------------------------------
{formatted_details}

🛡 Recommended Action:
----------------------------------------
{recommended_action}

----------------------------------------
This alert was generated automatically by
Security Risk Detection System.
Timestamp: {datetime.utcnow()}
----------------------------------------
"""

        send_alert_email(
            receiver_email="sreeja.warangal834@gmail.com",
            subject=f"{severity} Security Alert Detected",
            body=body
        )

    return result

