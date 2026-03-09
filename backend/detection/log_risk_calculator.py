# backend/detection/risk_engine.py

def calculate_log_risk(severity, exposure=1, asset_value=1):
    """
    Calculates risk score based on:
    - severity level
    - exposure factor
    - asset value

    Returns a normalized score out of 10.
    """

    severity_map = {
        "INFO": 1,
        "WARNING": 5,
        "ERROR": 9
    }

    base_score = severity_map.get(severity.upper(), 1)

    risk_score = base_score * exposure * asset_value

    # Normalize to max 10
    return min(round(risk_score, 2), 10)
