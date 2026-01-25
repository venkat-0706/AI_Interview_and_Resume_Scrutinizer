# Email service
import smtplib
from email.message import EmailMessage
from app.core.config import MONGO_URI  # just to confirm config import works
import os

# Email configuration (load from environment)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USER)


def send_email(to: str, subject: str, body: str) -> bool:
    """
    Send a plain text email.

    Args:
        to (str): Recipient email address
        subject (str): Email subject
        body (str): Email body

    Returns:
        bool: True if email sent successfully, else False
    """
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_FROM
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        print(f"[EMAIL SERVICE] Email sent to {to}")
        return True

    except Exception as e:
        print(f"[EMAIL SERVICE ERROR] {e}")
        return False
