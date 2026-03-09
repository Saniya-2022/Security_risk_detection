import json
from datetime import datetime, timezone
from backend.detection.risk_engine import calculate_risk
from backend.database.mongo import save_alert
from backend.intelligence.cve_service import fetch_cve_data


def generate_alert(finding):
    rule_id = finding.get("check_id")
    file_path = finding.get("path")
    line = finding.get("start", {}).get("line")
    message = finding.get("extra", {}).get("message")
    severity = finding.get("extra", {}).get("severity", "INFO")

    # Base Risk
    risk_score = calculate_risk(
        severity,
        exposure=1.5,
        asset_value=2
    )

    # CVE Enrichment
    cve_data = fetch_cve_data(message)

    if cve_data:
        cvss = cve_data.get("cvss_score", 0)
        risk_score = min(risk_score + (cvss / 2), 10)
    else:
        cve_data = {}

    alert = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "file": file_path,
        "line": line,
        "rule_id": rule_id,
        "severity": severity,
        "risk_score": risk_score,
        "description": message,
        "cve_id": cve_data.get("cve_id"),
        "cvss_score": cve_data.get("cvss_score"),
        "human_readable_alert": f"""
⚠ SECURITY ALERT

File: {file_path}
Line: {line}
Rule ID: {rule_id}
Severity: {severity}
Risk Score: {risk_score}/10

Issue:
{message}

Recommendation:
Review this code immediately and apply secure coding best practices.
"""
    }

    return alert


def main():
    try:
        with open("results.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ results.json not found.")
        return

    findings = data.get("results", [])

    print("Total findings:", len(findings))

    alerts = []

    for finding in findings:
        alert = generate_alert(finding)

        result = save_alert(alert)
        alert["_id"] = str(result.inserted_id)

        alerts.append(alert)

    with open("alerts.json", "w") as f:
        json.dump(alerts, f, indent=4)

    print(f"✅ Generated {len(alerts)} human-readable alerts.")


if __name__ == "__main__":
    main()
