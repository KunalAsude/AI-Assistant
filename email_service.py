"""
Email functionality for the voice assistant
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Tuple
import config

class EmailService:
    def __init__(self):
        """Initialize the email service"""
        self.email_user = config.EMAIL_USER
        self.email_password = config.EMAIL_PASSWORD
        self.smtp_server = config.EMAIL_SMTP_SERVER
        self.smtp_port = config.EMAIL_SMTP_PORT
        
    def send_email(self, to_email: str, subject: str, body: str) -> Tuple[bool, str]:
        """
        Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body text
            
        Returns:
            Tuple[bool, str]: Success status and message
        """
        if not self.email_user or not self.email_password:
            return False, "Email credentials not configured. Please set EMAIL_USER and EMAIL_PASSWORD in .env file."
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.login(self.email_user, self.email_password)
            
            text = msg.as_string()
            server.sendmail(self.email_user, to_email, text)
            server.close()
            
            return True, f"Email sent successfully to {to_email}"
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
