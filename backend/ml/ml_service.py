"""
Enhanced ML Service for Mini SIEM
Provides predictions for all detection modules
"""

import joblib
import os
import numpy as np

BASE_DIR = os.path.dirname(__file__)

# ============================================
# LOAD ALL TRAINED MODELS
# ============================================

try:
    phishing_model = joblib.load(os.path.join(BASE_DIR, "models/phishing_model.pkl"))
    phishing_vectorizer = joblib.load(os.path.join(BASE_DIR, "models/phishing_vectorizer.pkl"))
    print("✅ Phishing model loaded")
except:
    print("⚠️ Phishing model not found - using fallback")
    phishing_model = None
    phishing_vectorizer = None

try:
    login_model = joblib.load(os.path.join(BASE_DIR, "models/login_model.pkl"))
    print("✅ Login model loaded")
except:
    print("⚠️ Login model not found - using fallback")
    login_model = None

try:
    network_model = joblib.load(os.path.join(BASE_DIR, "models/network_model.pkl"))
    print("✅ Network model loaded")
except:
    print("⚠️ Network model not found - using fallback")
    network_model = None

try:
    malware_model = joblib.load(os.path.join(BASE_DIR, "models/malware_model.pkl"))
    print("✅ Malware model loaded")
except:
    print("⚠️ Malware model not found - using fallback")
    malware_model = None


# ============================================
# 1. PHISHING DETECTION
# ============================================

def predict_phishing_ml(email_data):
    """Predict if email is phishing using ML"""
    
    if phishing_model is None or phishing_vectorizer is None:
        return {"is_phishing": False, "probability": 0.0}
    
    try:
        # Create text features
        text = f"{email_data.get('sender', '')} {email_data.get('subject', '')} {email_data.get('body', '')}"
        X_text = phishing_vectorizer.transform([text])
        
        # Add numerical features
        num_links = email_data.get('num_links', 0)
        suspicious_keywords = email_data.get('suspicious_keywords', 0)
        X_numerical = np.array([[num_links, suspicious_keywords]])
        
        # Combine features
        X = np.hstack([X_text.toarray(), X_numerical])
        
        # Predict
        probability = phishing_model.predict_proba(X)[0][1]
        prediction = phishing_model.predict(X)[0]
        
        return {
            "is_phishing": bool(prediction),
            "probability": float(probability)
        }
    except Exception as e:
        print(f"Error in phishing prediction: {e}")
        return {"is_phishing": False, "probability": 0.0}


# ============================================
# 2. LOGIN ANOMALY DETECTION
# ============================================

def predict_login_anomaly(login_data):
    """Predict if login attempt is anomalous"""
    
    if login_model is None:
        return {"is_anomaly": False, "probability": 0.0}
    
    try:
        # Encode country
        country_map = {"US": 0, "UK": 1, "CA": 2, "DE": 3, "FR": 4, "CN": 5, "RU": 6, "KP": 7, "IR": 8}
        country_encoded = country_map.get(login_data.get('country', 'US'), 0)
        
        # Create feature vector
        X = np.array([[
            login_data.get('failed_attempts', 0),
            login_data.get('time_of_login', 12),
            login_data.get('login_frequency', 1),
            country_encoded
        ]])
        
        # Predict
        if hasattr(login_model, 'predict_proba'):
            probability = login_model.predict_proba(X)[0][1]
            prediction = login_model.predict(X)[0]
        else:
            # Isolation Forest returns -1 for anomaly
            prediction = login_model.predict(X)[0]
            prediction = 1 if prediction == -1 else 0
            probability = 0.8 if prediction == 1 else 0.2
        
        return {
            "is_anomaly": bool(prediction),
            "probability": float(probability),
            "threat_type": "Brute Force" if prediction else "Normal"
        }
    except Exception as e:
        print(f"Error in login prediction: {e}")
        return {"is_anomaly": False, "probability": 0.0}


# ============================================
# 3. NETWORK TRAFFIC CLASSIFICATION
# ============================================

def predict_network_traffic(traffic_data):
    """Classify network traffic"""
    
    if network_model is None:
        return {"attack_type": "Normal", "label": 0, "probability": 0.0}
    
    try:
        # Encode protocol
        protocol_map = {"TCP": 0, "UDP": 1, "ICMP": 2, "HTTP": 3, "HTTPS": 4}
        protocol_encoded = protocol_map.get(traffic_data.get('protocol', 'TCP'), 0)
        
        # Create feature vector
        X = np.array([[
            traffic_data.get('request_count_per_min', 10),
            traffic_data.get('port_number', 80),
            traffic_data.get('packet_size', 1000),
            protocol_encoded,
            traffic_data.get('duration', 10)
        ]])
        
        # Predict
        prediction = network_model.predict(X)[0]
        
        if hasattr(network_model, 'predict_proba'):
            probabilities = network_model.predict_proba(X)[0]
            probability = float(max(probabilities))
        else:
            probability = 0.9 if prediction > 0 else 0.1
        
        # Map label to attack type
        attack_types = {0: "Normal", 1: "DoS", 2: "Probe", 3: "BruteForce"}
        attack_type = attack_types.get(prediction, "Normal")
        
        return {
            "attack_type": attack_type,
            "label": int(prediction),
            "probability": probability
        }
    except Exception as e:
        print(f"Error in network prediction: {e}")
        return {"attack_type": "Normal", "label": 0, "probability": 0.0}


# ============================================
# 4. MALWARE DETECTION
# ============================================

def predict_malware(file_data):
    """Predict if file is malware"""
    
    if malware_model is None:
        return {"is_malware": False, "probability": 0.0}
    
    try:
        # Encode extension
        extension_map = {"txt": 0, "pdf": 1, "docx": 2, "jpg": 3, "png": 4, 
                        "exe": 5, "bat": 6, "scr": 7, "vbs": 8, "js": 9}
        extension = file_data.get('extension', 'txt')
        extension_encoded = extension_map.get(extension, 0)
        
        # Create feature vector
        X = np.array([[
            extension_encoded,
            file_data.get('file_size', 1000),
            file_data.get('encoded_patterns', 0),
            file_data.get('suspicious_script', 0)
        ]])
        
        # Predict
        probability = malware_model.predict_proba(X)[0][1]
        prediction = malware_model.predict(X)[0]
        
        return {
            "is_malware": bool(prediction),
            "probability": float(probability)
        }
    except Exception as e:
        print(f"Error in malware prediction: {e}")
        return {"is_malware": False, "probability": 0.0}
