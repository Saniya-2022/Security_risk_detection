from collections import defaultdict
from datetime import datetime, timezone
from backend.database.mongo import save_alert

FAILED_THRESHOLD = 5
failed_attempts = defaultdict(int)


def monitor_login_event(log):
    alerts = []

    if log.get("event") == "login" and log.get("status") == "failed":
        key = (log.get("user"), log.get("ip"))
        failed_attempts[key] += 1

        if failed_attempts[key] >= FAILED_THRESHOLD:
            alert = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": "Runtime Threat",
                "threat": "Brute Force Attack",
                "user": log.get("user"),
                "ip": log.get("ip"),
                "risk_score": 9,
                "severity": "CRITICAL",
                "description": f"Multiple failed login attempts detected for user {log.get('user')} from IP {log.get('ip')}.",
                "human_readable_alert": f"""
🚨 RUNTIME SECURITY ALERT

Threat: Brute Force Attack
User: {log.get('user')}
Source IP: {log.get('ip')}
Severity: CRITICAL
Risk Score: 9/10

Recommended Action:
• Block the source IP
• Lock the account temporarily
• Enable MFA
"""
            }

            result = save_alert(alert)
            alert["_id"] = str(result.inserted_id)
            alerts.append(alert)

    return alerts
