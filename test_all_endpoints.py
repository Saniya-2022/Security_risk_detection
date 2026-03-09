"""
Comprehensive Test Script for Mini SIEM API
Tests all detection endpoints with sample data
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_result(response, test_name):
    print(f"\n🧪 Test: {test_name}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Threat Type: {data.get('threat_type', 'N/A')}")
        print(f"Risk Score: {data.get('risk_score', 'N/A')}/100")
        print(f"Severity: {data.get('severity', 'N/A')}")
        print(f"ML Probability: {data.get('ml_probability', 'N/A')}")
        print(f"Is Threat: {data.get('is_threat', 'N/A')}")
        
        if 'human_readable_alert' in data:
            print(f"\nAlert Message:")
            print(data['human_readable_alert'][:200] + "...")
    else:
        print(f"❌ Failed: {response.text}")
    
    print("-" * 70)

def test_system_status():
    print_header("Testing System Status")
    try:
        response = requests.get(f"{BASE_URL}/system/status")
        print_result(response, "System Status Check")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_phishing_detection():
    print_header("Testing Phishing Detection")
    
    # Test 1: High-risk phishing email
    test_data_1 = {
        "sender": "urgent@secure-bank.tk",
        "subject": "URGENT: Verify your account immediately",
        "body": "Dear user, your account has been suspended. Click here to verify: http://malicious-link.com",
        "num_links": 5,
        "suspicious_keywords": 6
    }
    
    try:
        response = requests.post(f"{BASE_URL}/detect/phishing", json=test_data_1)
        print_result(response, "High-Risk Phishing Email")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # Test 2: Legitimate email
    test_data_2 = {
        "sender": "newsletter@company.com",
        "subject": "Monthly Newsletter",
        "body": "Here is your monthly update from our team.",
        "num_links": 1,
        "suspicious_keywords": 0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/detect/phishing", json=test_data_2)
        print_result(response, "Legitimate Email")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_login_detection():
    print_header("Testing Login Anomaly Detection")
    
    # Test 1: Brute force attack
    test_data_1 = {
        "ip_address": "192.168.1.100",
        "username": "admin",
        "failed_attempts": 15,
        "time_of_login": 3,
        "country": "RU",
        "login_frequency": 200
    }
    
    try:
        response = requests.post(f"{BASE_URL}/detect/login", json=test_data_1)
        print_result(response, "Brute Force Attack")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # Test 2: Normal login
    test_data_2 = {
        "ip_address": "10.0.0.50",
        "username": "john.doe",
        "failed_attempts": 0,
        "time_of_login": 14,
        "country": "US",
        "login_frequency": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/detect/login", json=test_data_2)
        print_result(response, "Normal Login")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_network_detection():
    print_header("Testing Network Traffic Classification")
    
    # Test 1: DoS attack
    test_data_1 = {
        "ip_address": "203.0.113.50",
        "request_count_per_min": 1500,
        "port_number": 80,
        "packet_size": 50,
        "protocol": "TCP",
        "duration": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/detect/network", json=test_data_1)
        print_result(response, "DoS Attack")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # Test 2: Port scanning
    test_data_2 = {
        "ip_address": "198.51.100.25",
        "request_count_per_min": 200,
        "port_number": 22,
        "packet_size": 100,
        "protocol": "TCP",
        "duration": 60
    }
    
    try:
        response = requests.post(f"{BASE_URL}/detect/network", json=test_data_2)
        print_result(response, "Port Scanning")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # Test 3: Normal traffic
    test_data_3 = {
        "ip_address": "192.168.1.50",
        "request_count_per_min": 20,
        "port_number": 443,
        "packet_size": 1200,
        "protocol": "HTTPS",
        "duration": 30
    }
    
    try:
        response = requests.post(f"{BASE_URL}/detect/network", json=test_data_3)
        print_result(response, "Normal Traffic")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_malware_detection():
    print_header("Testing Malware Detection")
    
    # Test 1: Malicious file
    test_data_1 = {
        "file_name": "suspicious.exe",
        "extension": "exe",
        "file_size": 500000,
        "encoded_patterns": 15,
        "suspicious_script": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/detect/malware", json=test_data_1)
        print_result(response, "Malicious Executable")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # Test 2: Safe file
    test_data_2 = {
        "file_name": "document.pdf",
        "extension": "pdf",
        "file_size": 50000,
        "encoded_patterns": 0,
        "suspicious_script": 0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/detect/malware", json=test_data_2)
        print_result(response, "Safe PDF Document")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_alert_retrieval():
    print_header("Testing Alert Retrieval")
    
    try:
        # Get all alerts
        response = requests.get(f"{BASE_URL}/alerts?limit=10")
        if response.status_code == 200:
            alerts = response.json()
            print(f"✅ Retrieved {len(alerts)} alerts")
            if alerts:
                print(f"Latest alert: {alerts[0].get('threat_type')} - {alerts[0].get('severity')}")
        else:
            print(f"❌ Failed to retrieve alerts: {response.text}")
        
        # Get statistics
        response = requests.get(f"{BASE_URL}/alerts/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"\n📊 Alert Statistics:")
            print(f"Total Alerts: {stats.get('total_alerts', 0)}")
            print(f"HIGH: {stats.get('by_severity', {}).get('HIGH', 0)}")
            print(f"MEDIUM: {stats.get('by_severity', {}).get('MEDIUM', 0)}")
            print(f"LOW: {stats.get('by_severity', {}).get('LOW', 0)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_ip_management():
    print_header("Testing IP Management")
    
    try:
        # Get blocked IPs
        response = requests.get(f"{BASE_URL}/security/blocked-ips")
        if response.status_code == 200:
            blocked_ips = response.json()
            print(f"✅ Currently blocked IPs: {len(blocked_ips)}")
            for ip in blocked_ips[:5]:
                print(f"  - {ip['ip_address']}: {ip['reason']}")
        else:
            print(f"❌ Failed to retrieve blocked IPs: {response.text}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("\n" + "="*70)
    print("  🧪 Mini SIEM - Comprehensive API Testing Suite")
    print("="*70)
    print(f"\nTesting API at: {BASE_URL}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("\n❌ Error: API server is not responding!")
            print("Please start the server with:")
            print("uvicorn backend.api.main_enhanced:app --reload --host 0.0.0.0 --port 8000")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server!")
        print("Please start the server with:")
        print("uvicorn backend.api.main_enhanced:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Run all tests
    test_system_status()
    test_phishing_detection()
    test_login_detection()
    test_network_detection()
    test_malware_detection()
    test_alert_retrieval()
    test_ip_management()
    
    print("\n" + "="*70)
    print("  ✅ All Tests Completed!")
    print("="*70)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 Check the dashboard at http://localhost:3000 to see real-time alerts!")

if __name__ == "__main__":
    main()
