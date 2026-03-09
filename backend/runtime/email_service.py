import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import logging
from typing import Dict, Any

load_dotenv()

logger = logging.getLogger(__name__)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


class EmailService:
    """Email service for sending alert notifications"""
    
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.sender_email = SENDER_EMAIL
        self.sender_password = SENDER_PASSWORD
        
        if not self.sender_email or not self.sender_password:
            logger.warning("⚠️ Email credentials missing in .env - email alerts disabled")
    
    async def send_alert_email(self, subject: str, body: str, alert_data: Dict[str, Any] = None):
        """Send alert email asynchronously"""
        receiver_email = os.getenv("RECEIVER_EMAIL", self.sender_email)
        return self._send_email(receiver_email, subject, body)
    
    def _send_email(self, receiver_email: str, subject: str, body: str) -> bool:
        """Internal method to send email"""
        if not self.sender_email or not self.sender_password:
            return False
        
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            
            message.attach(MIMEText(body, "plain"))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
            server.quit()
            
            logger.info(f"✅ Alert email sent to {receiver_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("❌ SMTP Authentication failed")
            return False
        except Exception as e:
            logger.error(f"❌ Email send failed: {e}")
            return False


def send_alert_email(receiver_email, subject, body):
    """Send email alert with proper error handling (legacy function)"""
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        logger.warning("⚠️ Email credentials missing in .env - skipping email notification")
        return False
    
    try:
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        server.quit()

        logger.info(f"✅ Alert email sent successfully to {receiver_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logger.error("❌ SMTP Authentication failed - check email credentials")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to send email: {e}")
        return False
