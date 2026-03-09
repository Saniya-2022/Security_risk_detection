from backend.detection.email_detector import analyze_email_attachment
from backend.risk_engine import process_security_events
from backend.ml.ml_service import predict_phishing_ml


def detect_phishing(email_data):

    events = []

    # -------------------------------
    # Rule-Based Attachment Check
    # -------------------------------
    if email_data.get("attachment"):
        attachment_event = analyze_email_attachment(email_data["attachment"])
        if attachment_event:
            events.append(attachment_event)

    rule_result = process_security_events(events)

    # -------------------------------
    # ML Detection
    # -------------------------------
    ml_result = predict_phishing_ml(email_data)

    # -------------------------------
    # Combine Both
    # -------------------------------
    final_score = rule_result.get("total_score", 0)

    if ml_result["is_phishing"]:
        final_score += int(ml_result["probability"] * 50)

    # Severity Calculation
    if final_score >= 80:
        severity = "CRITICAL"
    elif final_score >= 60:
        severity = "HIGH"
    elif final_score >= 40:
        severity = "MEDIUM"
    else:
        severity = "INFO"

    return {
        "total_score": final_score,
        "severity": severity,
        "ml_probability": ml_result["probability"],
        "alert": {
            "details": [
                f"ML phishing probability: {round(ml_result['probability'] * 100, 2)}%",
                "Hybrid Detection Used (Rule + ML)"
            ],
            "recommended_action": "Do not click links. Verify sender authenticity. Report to SOC team."
        }
    }
