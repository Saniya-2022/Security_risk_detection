import joblib

model = joblib.load("phishing_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


def detect_phishing_ml(email_data):

    text = f"{email_data.get('subject', '')} {email_data.get('body', '')}"

    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)[0]
    probability = model.predict_proba(text_vector)[0][1]

    if prediction == 1:
        severity = "HIGH" if probability > 0.8 else "MEDIUM"

        return {
            "type": "ml_phishing",
            "total_score": round(probability * 100),
            "severity": severity,
            "alert": {
                "details": [
                    f"ML model detected phishing probability: {round(probability * 100)}%"
                ],
                "recommended_action": "Do not click links. Verify sender identity."
            }
        }

    return None
