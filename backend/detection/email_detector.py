SUSPICIOUS_EXTENSIONS = [".exe", ".js", ".vbs", ".scr", ".bat", ".zip", ".docm"]


def analyze_email_attachment(filename):

    if not filename:
        return None

    risk_score = 0
    reasons = []

    # 1️⃣ Check suspicious extension
    if any(filename.lower().endswith(ext) for ext in SUSPICIOUS_EXTENSIONS):
        risk_score += 40
        reasons.append(f"Suspicious attachment type detected: {filename}")

    # 2️⃣ Check double extension (invoice.pdf.exe)
    if filename.count(".") > 1:
        risk_score += 20
        reasons.append("Possible double extension file")

    # If no risk found → return None (important)
    if risk_score == 0:
        return None

    return {
        "type": "malicious_attachment",
        "score": risk_score,
        "reason": " | ".join(reasons)
    }
