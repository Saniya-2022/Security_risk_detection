"""
Real-Time Event Generator for Mini SIEM
Continuously generates realistic security events
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class EventGenerator:
    """Generates realistic security events continuously"""
    
    def __init__(self):
        self.running = False
        self.suspicious_ips = [
            "192.168.1.100", "203.0.113.50", "198.51.100.25",
            "10.0.0.99", "172.16.0.50", "45.33.32.156"
        ]
        self.normal_ips = [
            "192.168.1.50", "10.0.0.25", "172.16.0.10",
            "192.168.1.75", "10.0.0.30"
        ]
        self.usernames = ["admin", "root", "user", "john.doe", "jane.smith", "test"]
        self.countries = ["US", "UK", "CA", "DE", "FR", "RU", "CN", "KP", "IR"]
        self.protocols = ["TCP", "UDP", "HTTP", "HTTPS", "ICMP"]
        self.file_extensions = ["exe", "bat", "scr", "pdf", "docx", "txt", "jpg"]
        
        # Phishing email templates
        self.phishing_subjects = [
            "URGENT: Verify your account immediately",
            "Your account has been suspended",
            "Action Required: Security Alert",
            "You've won a prize!",
            "Confirm your identity now",
            "Important: Update your password"
        ]
        
        self.phishing_senders = [
            "urgent@secure-bank.tk",
            "security@paypal-verify.ml",
            "noreply@amazon-alert.ga",
            "support@microsoft-update.cf"
        ]
        
        self.legitimate_subjects = [
            "Monthly Newsletter",
            "Team Meeting Tomorrow",
            "Project Update",
            "Weekly Report"
        ]
        
        self.legitimate_senders = [
            "newsletter@company.com",
            "team@organization.com",
            "updates@service.com"
        ]
    
    async def generate_login_event(self) -> Dict[str, Any]:
        """Generate a login attempt event"""
        
        # 30% chance of suspicious activity
        is_suspicious = random.random() < 0.3
        
        if is_suspicious:
            ip = random.choice(self.suspicious_ips)
            failed_attempts = random.randint(5, 20)
            time_of_login = random.randint(0, 5)  # Late night
            country = random.choice(["RU", "CN", "KP", "IR"])
            login_frequency = random.randint(50, 200)
        else:
            ip = random.choice(self.normal_ips)
            failed_attempts = random.randint(0, 2)
            time_of_login = random.randint(8, 18)  # Business hours
            country = random.choice(["US", "UK", "CA", "DE", "FR"])
            login_frequency = random.randint(1, 10)
        
        return {
            "event_type": "login",
            "ip_address": ip,
            "username": random.choice(self.usernames),
            "failed_attempts": failed_attempts,
            "time_of_login": time_of_login,
            "country": country,
            "login_frequency": login_frequency,
            "timestamp": datetime.utcnow()
        }
    
    async def generate_network_event(self) -> Dict[str, Any]:
        """Generate a network traffic event"""
        
        # 25% chance of attack
        attack_type = random.choices(
            ["Normal", "DoS", "Probe", "BruteForce"],
            weights=[0.75, 0.10, 0.10, 0.05]
        )[0]
        
        if attack_type == "DoS":
            ip = random.choice(self.suspicious_ips)
            request_count = random.randint(500, 2000)
            packet_size = random.randint(1, 100)
            duration = random.randint(1, 10)
            port = random.choice([80, 443, 8080])
        elif attack_type == "Probe":
            ip = random.choice(self.suspicious_ips)
            request_count = random.randint(100, 300)
            packet_size = random.randint(50, 200)
            duration = random.randint(30, 120)
            port = random.randint(1, 65535)
        elif attack_type == "BruteForce":
            ip = random.choice(self.suspicious_ips)
            request_count = random.randint(50, 150)
            packet_size = random.randint(100, 500)
            duration = random.randint(10, 60)
            port = random.choice([22, 21, 3389])
        else:  # Normal
            ip = random.choice(self.normal_ips)
            request_count = random.randint(1, 50)
            packet_size = random.randint(500, 1500)
            duration = random.randint(1, 300)
            port = random.choice([80, 443])
        
        return {
            "event_type": "network",
            "ip_address": ip,
            "request_count_per_min": request_count,
            "port_number": port,
            "packet_size": packet_size,
            "protocol": random.choice(self.protocols),
            "duration": duration,
            "attack_classification": attack_type,
            "timestamp": datetime.utcnow()
        }
    
    async def generate_email_event(self) -> Dict[str, Any]:
        """Generate an email event"""
        
        # 35% chance of phishing
        is_phishing = random.random() < 0.35
        
        if is_phishing:
            sender = random.choice(self.phishing_senders)
            subject = random.choice(self.phishing_subjects)
            body = f"Dear user, {subject.lower()}. Click here: http://malicious-link.com"
            num_links = random.randint(3, 10)
            suspicious_keywords = random.randint(3, 8)
            attachment = random.choice(["invoice.exe", "document.scr", ""])
        else:
            sender = random.choice(self.legitimate_senders)
            subject = random.choice(self.legitimate_subjects)
            body = "This is a legitimate email with normal content."
            num_links = random.randint(0, 2)
            suspicious_keywords = random.randint(0, 1)
            attachment = random.choice(["report.pdf", "document.docx", ""])
        
        return {
            "event_type": "email",
            "sender": sender,
            "subject": subject,
            "body": body,
            "attachment": attachment,
            "num_links": num_links,
            "suspicious_keywords": suspicious_keywords,
            "timestamp": datetime.utcnow()
        }
    
    async def generate_malware_event(self) -> Dict[str, Any]:
        """Generate a file scan event"""
        
        # 20% chance of malware
        is_malware = random.random() < 0.2
        
        if is_malware:
            extension = random.choice(["exe", "bat", "scr", "vbs", "js"])
            file_size = random.randint(10000, 5000000)
            encoded_patterns = random.randint(5, 20)
            suspicious_script = 1
        else:
            extension = random.choice(["pdf", "docx", "txt", "jpg", "png"])
            file_size = random.randint(1000, 1000000)
            encoded_patterns = random.randint(0, 2)
            suspicious_script = 0
        
        filename = f"file_{random.randint(1000, 9999)}.{extension}"
        
        return {
            "event_type": "malware",
            "file_name": filename,
            "extension": extension,
            "file_size": file_size,
            "encoded_patterns": encoded_patterns,
            "suspicious_script": suspicious_script,
            "timestamp": datetime.utcnow()
        }
    
    async def generate_random_event(self) -> Dict[str, Any]:
        """Generate a random security event"""
        
        event_types = [
            self.generate_login_event,
            self.generate_network_event,
            self.generate_email_event,
            self.generate_malware_event
        ]
        
        # Weight towards login and network events (more common)
        weights = [0.35, 0.35, 0.20, 0.10]
        generator = random.choices(event_types, weights=weights)[0]
        
        return await generator()
    
    async def start(self, callback):
        """Start generating events continuously"""
        self.running = True
        logger.info("🚀 Event Generator started - generating live security events")
        
        while self.running:
            try:
                # Generate random event
                event = await self.generate_random_event()
                
                # Call the callback to process the event
                await callback(event)
                
                # Wait 1-2 seconds before next event (faster for demo)
                await asyncio.sleep(random.uniform(1, 2))
                
            except Exception as e:
                logger.error(f"Error generating event: {e}")
                await asyncio.sleep(5)
    
    def stop(self):
        """Stop generating events"""
        self.running = False
        logger.info("🛑 Event Generator stopped")


# Global instance
event_generator = EventGenerator()
