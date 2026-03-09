"""
Synthetic Dataset Generator for Mini SIEM
Generates realistic training data for all detection modules
"""

import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import json

fake = Faker()

# ============================================
# A) EMAIL SECURITY DATASET
# ============================================

def generate_email_dataset(num_samples=500):
    """Generate synthetic email dataset for phishing detection"""
    
    phishing_keywords = [
        "urgent", "verify", "suspended", "click here", "confirm", 
        "account", "password", "security alert", "prize", "winner",
        "bank", "credit card", "social security", "tax refund"
    ]
    
    legitimate_domains = ["gmail.com", "yahoo.com", "outlook.com", "company.com"]
    suspicious_domains = ["secure-bank.tk", "verify-account.ml", "prize-winner.ga"]
    
    data = []
    
    for i in range(num_samples):
        is_phishing = random.choice([True, False])
        
        if is_phishing:
            subject = f"{random.choice(['URGENT', 'ACTION REQUIRED', 'VERIFY NOW'])}: {random.choice(phishing_keywords)}"
            body = f"Dear user, {random.choice(phishing_keywords)} your account immediately. Click here: http://malicious-link.com"
            sender_domain = random.choice(suspicious_domains)
            num_links = random.randint(3, 10)
            suspicious_keywords_count = random.randint(3, 8)
            attachment_type = random.choice(["exe", "zip", "scr", "none"])
            label = 1
        else:
            subject = fake.sentence()
            body = fake.text(max_nb_chars=200)
            sender_domain = random.choice(legitimate_domains)
            num_links = random.randint(0, 2)
            suspicious_keywords_count = random.randint(0, 1)
            attachment_type = random.choice(["pdf", "docx", "none", "none"])
            label = 0
        
        data.append({
            "subject": subject,
            "body": body,
            "sender_domain": sender_domain,
            "num_links": num_links,
            "suspicious_keywords": suspicious_keywords_count,
            "attachment_type": attachment_type,
            "label": label
        })
    
    df = pd.DataFrame(data)
    df.to_csv("backend/datasets/email_dataset.csv", index=False)
    print(f"✅ Generated {num_samples} email samples")
    return df


# ============================================
# B) LOGIN ACTIVITY DATASET
# ============================================

def generate_login_dataset(num_samples=500):
    """Generate synthetic login activity dataset"""
    
    normal_countries = ["US", "UK", "CA", "DE", "FR"]
    suspicious_countries = ["CN", "RU", "KP", "IR"]
    
    data = []
    
    for i in range(num_samples):
        is_attack = random.choice([True, False])
        
        if is_attack:
            ip = fake.ipv4()
            failed_attempts = random.randint(5, 20)
            country = random.choice(suspicious_countries)
            login_frequency = random.randint(50, 200)
            time_of_login = random.randint(0, 5)  # Late night
            label = 1  # Brute Force
        else:
            ip = fake.ipv4()
            failed_attempts = random.randint(0, 2)
            country = random.choice(normal_countries)
            login_frequency = random.randint(1, 10)
            time_of_login = random.randint(8, 18)  # Business hours
            label = 0  # Normal
        
        data.append({
            "ip_address": ip,
            "failed_attempts": failed_attempts,
            "time_of_login": time_of_login,
            "country": country,
            "login_frequency": login_frequency,
            "label": label
        })
    
    df = pd.DataFrame(data)
    df.to_csv("backend/datasets/login_dataset.csv", index=False)
    print(f"✅ Generated {num_samples} login samples")
    return df


# ============================================
# C) NETWORK TRAFFIC DATASET
# ============================================

def generate_network_dataset(num_samples=1000):
    """Generate synthetic network traffic dataset"""
    
    protocols = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS"]
    
    data = []
    
    for i in range(num_samples):
        attack_type = random.choice(["Normal", "DoS", "Probe", "BruteForce"])
        
        if attack_type == "DoS":
            request_count = random.randint(500, 2000)
            packet_size = random.randint(1, 100)
            duration = random.randint(1, 10)
            port = random.choice([80, 443, 8080])
            label = 1
        elif attack_type == "Probe":
            request_count = random.randint(100, 300)
            packet_size = random.randint(50, 200)
            duration = random.randint(30, 120)
            port = random.randint(1, 65535)
            label = 2
        elif attack_type == "BruteForce":
            request_count = random.randint(50, 150)
            packet_size = random.randint(100, 500)
            duration = random.randint(10, 60)
            port = random.choice([22, 21, 3389])
            label = 3
        else:  # Normal
            request_count = random.randint(1, 50)
            packet_size = random.randint(500, 1500)
            duration = random.randint(1, 300)
            port = random.choice([80, 443])
            label = 0
        
        data.append({
            "ip_address": fake.ipv4(),
            "request_count_per_min": request_count,
            "port_number": port,
            "packet_size": packet_size,
            "protocol": random.choice(protocols),
            "duration": duration,
            "label": label,
            "attack_type": attack_type
        })
    
    df = pd.DataFrame(data)
    df.to_csv("backend/datasets/network_dataset.csv", index=False)
    print(f"✅ Generated {num_samples} network traffic samples")
    return df


# ============================================
# D) MALWARE DETECTION DATASET
# ============================================

def generate_malware_dataset(num_samples=500):
    """Generate synthetic malware detection dataset"""
    
    safe_extensions = ["txt", "pdf", "docx", "jpg", "png"]
    malicious_extensions = ["exe", "bat", "scr", "vbs", "js"]
    
    data = []
    
    for i in range(num_samples):
        is_malware = random.choice([True, False])
        
        if is_malware:
            extension = random.choice(malicious_extensions)
            file_size = random.randint(10000, 5000000)
            suspicious_patterns = random.randint(5, 20)
            has_script = 1
            label = 1
        else:
            extension = random.choice(safe_extensions)
            file_size = random.randint(1000, 1000000)
            suspicious_patterns = random.randint(0, 2)
            has_script = 0
            label = 0
        
        data.append({
            "file_name": fake.file_name(extension=extension),
            "extension": extension,
            "file_size": file_size,
            "encoded_patterns": suspicious_patterns,
            "suspicious_script": has_script,
            "label": label
        })
    
    df = pd.DataFrame(data)
    df.to_csv("backend/datasets/malware_dataset.csv", index=False)
    print(f"✅ Generated {num_samples} malware samples")
    return df


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("🔄 Generating synthetic datasets for Mini SIEM...\n")
    
    email_df = generate_email_dataset(500)
    login_df = generate_login_dataset(500)
    network_df = generate_network_dataset(1000)
    malware_df = generate_malware_dataset(500)
    
    print("\n✅ All datasets generated successfully!")
    print("\nDataset Summary:")
    print(f"📧 Email Dataset: {len(email_df)} samples")
    print(f"🔐 Login Dataset: {len(login_df)} samples")
    print(f"🌐 Network Dataset: {len(network_df)} samples")
    print(f"🦠 Malware Dataset: {len(malware_df)} samples")
