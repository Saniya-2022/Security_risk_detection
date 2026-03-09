import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Sample dataset (replace with real dataset later)
data = {
    "text": [
        "Verify your bank account immediately",
        "Urgent! Click here to reset your password",
        "Meeting scheduled tomorrow",
        "Invoice attached please review",
        "Congratulations you won lottery click now",
        "Team meeting agenda attached"
    ],
    "label": [1, 1, 0, 0, 1, 0]  # 1 = phishing, 0 = legitimate
}

df = pd.DataFrame(data)

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Evaluate
X_test_tfidf = vectorizer.transform(X_test)
predictions = model.predict(X_test_tfidf)

print("Accuracy:", accuracy_score(y_test, predictions))

# Save model
joblib.dump(model, "phishing_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model trained and saved!")



