"""
Complete ML Model Training Pipeline for Mini SIEM
Trains all detection models with comparison and evaluation
"""

import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import os

# Create models directory
os.makedirs("backend/ml/models", exist_ok=True)

# ============================================
# 1. EMAIL PHISHING DETECTION MODEL
# ============================================

def train_phishing_model():
    print("\n" + "="*60)
    print("📧 TRAINING EMAIL PHISHING DETECTION MODEL")
    print("="*60)
    
    # Load dataset
    df = pd.read_csv("backend/datasets/email_dataset.csv")
    
    # Create text features
    df['text'] = df['subject'] + " " + df['body'] + " " + df['sender_domain']
    
    # Vectorization
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    X_text = vectorizer.fit_transform(df['text'])
    
    # Combine with numerical features
    X_numerical = df[['num_links', 'suspicious_keywords']].values
    X = np.hstack([X_text.toarray(), X_numerical])
    y = df['label'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Logistic Regression
    print("\n🔹 Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_accuracy = accuracy_score(y_test, lr_pred)
    print(f"   Accuracy: {lr_accuracy:.4f}")
    
    # Train Random Forest
    print("\n🔹 Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)
    print(f"   Accuracy: {rf_accuracy:.4f}")
    
    # Choose best model
    if rf_accuracy > lr_accuracy:
        best_model = rf_model
        best_name = "Random Forest"
        best_accuracy = rf_accuracy
    else:
        best_model = lr_model
        best_name = "Logistic Regression"
        best_accuracy = lr_accuracy
    
    print(f"\n✅ Best Model: {best_name} (Accuracy: {best_accuracy:.4f})")
    print("\nClassification Report:")
    print(classification_report(y_test, best_model.predict(X_test), 
                                target_names=['Legitimate', 'Phishing']))
    
    # Save model
    joblib.dump(best_model, "backend/ml/models/phishing_model.pkl")
    joblib.dump(vectorizer, "backend/ml/models/phishing_vectorizer.pkl")
    print("\n💾 Model saved: backend/ml/models/phishing_model.pkl")
    
    return best_accuracy


# ============================================
# 2. LOGIN ANOMALY DETECTION MODEL
# ============================================

def train_login_model():
    print("\n" + "="*60)
    print("🔐 TRAINING LOGIN ANOMALY DETECTION MODEL")
    print("="*60)
    
    # Load dataset
    df = pd.read_csv("backend/datasets/login_dataset.csv")
    
    # Encode country
    df['country_encoded'] = df['country'].astype('category').cat.codes
    
    # Features
    X = df[['failed_attempts', 'time_of_login', 'login_frequency', 'country_encoded']].values
    y = df['label'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    print("\n🔹 Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)
    print(f"   Accuracy: {rf_accuracy:.4f}")
    
    # Train Isolation Forest (for anomaly detection)
    print("\n🔹 Training Isolation Forest...")
    iso_model = IsolationForest(contamination=0.3, random_state=42)
    iso_model.fit(X_train)
    iso_pred = iso_model.predict(X_test)
    iso_pred = np.where(iso_pred == -1, 1, 0)  # Convert to binary
    iso_accuracy = accuracy_score(y_test, iso_pred)
    print(f"   Accuracy: {iso_accuracy:.4f}")
    
    # Choose best model
    if rf_accuracy > iso_accuracy:
        best_model = rf_model
        best_name = "Random Forest"
        best_accuracy = rf_accuracy
    else:
        best_model = iso_model
        best_name = "Isolation Forest"
        best_accuracy = iso_accuracy
    
    print(f"\n✅ Best Model: {best_name} (Accuracy: {best_accuracy:.4f})")
    print("\nClassification Report:")
    print(classification_report(y_test, rf_pred, 
                                target_names=['Normal', 'Brute Force']))
    
    # Save model
    joblib.dump(best_model, "backend/ml/models/login_model.pkl")
    print("\n💾 Model saved: backend/ml/models/login_model.pkl")
    
    return best_accuracy


# ============================================
# 3. NETWORK TRAFFIC CLASSIFICATION MODEL
# ============================================

def train_network_model():
    print("\n" + "="*60)
    print("🌐 TRAINING NETWORK TRAFFIC CLASSIFICATION MODEL")
    print("="*60)
    
    # Load dataset
    df = pd.read_csv("backend/datasets/network_dataset.csv")
    
    # Encode protocol
    df['protocol_encoded'] = df['protocol'].astype('category').cat.codes
    
    # Features
    X = df[['request_count_per_min', 'port_number', 'packet_size', 
            'protocol_encoded', 'duration']].values
    y = df['label'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Logistic Regression
    print("\n🔹 Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_accuracy = accuracy_score(y_test, lr_pred)
    print(f"   Accuracy: {lr_accuracy:.4f}")
    
    # Train Random Forest
    print("\n🔹 Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)
    print(f"   Accuracy: {rf_accuracy:.4f}")
    
    # Choose best model
    if rf_accuracy > lr_accuracy:
        best_model = rf_model
        best_name = "Random Forest"
        best_accuracy = rf_accuracy
    else:
        best_model = lr_model
        best_name = "Logistic Regression"
        best_accuracy = lr_accuracy
    
    print(f"\n✅ Best Model: {best_name} (Accuracy: {best_accuracy:.4f})")
    print("\nClassification Report:")
    print(classification_report(y_test, best_model.predict(X_test), 
                                target_names=['Normal', 'DoS', 'Probe', 'BruteForce']))
    
    # Save model
    joblib.dump(best_model, "backend/ml/models/network_model.pkl")
    print("\n💾 Model saved: backend/ml/models/network_model.pkl")
    
    return best_accuracy


# ============================================
# 4. MALWARE DETECTION MODEL
# ============================================

def train_malware_model():
    print("\n" + "="*60)
    print("🦠 TRAINING MALWARE DETECTION MODEL")
    print("="*60)
    
    # Load dataset
    df = pd.read_csv("backend/datasets/malware_dataset.csv")
    
    # Encode extension
    df['extension_encoded'] = df['extension'].astype('category').cat.codes
    
    # Features
    X = df[['extension_encoded', 'file_size', 'encoded_patterns', 'suspicious_script']].values
    y = df['label'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    print("\n🔹 Training Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)
    print(f"   Accuracy: {rf_accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, rf_pred, 
                                target_names=['Safe', 'Malware']))
    
    # Save model
    joblib.dump(rf_model, "backend/ml/models/malware_model.pkl")
    print("\n💾 Model saved: backend/ml/models/malware_model.pkl")
    
    return rf_accuracy


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 MINI SIEM - ML MODEL TRAINING PIPELINE")
    print("="*60)
    
    # Train all models
    phishing_acc = train_phishing_model()
    login_acc = train_login_model()
    network_acc = train_network_model()
    malware_acc = train_malware_model()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TRAINING SUMMARY")
    print("="*60)
    print(f"📧 Phishing Detection:  {phishing_acc:.4f}")
    print(f"🔐 Login Anomaly:       {login_acc:.4f}")
    print(f"🌐 Network Traffic:     {network_acc:.4f}")
    print(f"🦠 Malware Detection:   {malware_acc:.4f}")
    print("="*60)
    print("\n✅ All models trained and saved successfully!")
