import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Sample training dataset
data = {
    "text": [
        "Verify your bank account immediately",
        "Urgent click here to reset password",
        "Congratulations you won lottery",
        "Invoice attached please review",
        "Team meeting tomorrow at 10am",
        "Project discussion notes attached"
    ],
    "label": [1, 1, 1, 0, 0, 0]
}

df = pd.DataFrame(data)

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)

model = RandomForestClassifier(n_estimators=200)
model.fit(X_train_vec, y_train)

# Evaluation
X_test_vec = vectorizer.transform(X_test)
predictions = model.predict(X_test_vec)

print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "backend/ml/advanced_phishing_model.pkl")
joblib.dump(vectorizer, "backend/ml/advanced_vectorizer.pkl")

print("✅ Advanced ML model trained and saved")
