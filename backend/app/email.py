import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app
from flask_mail import Mail, Message


class EmailConfig:
    """Email configuration class"""

    # Update to use MailHog default settings
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = "noreply@quiznexus.com"


def configure_mail(app):
    """Configure Flask-Mail"""
    # Configure for MailHog instead of Gmail
    app.config["MAIL_SERVER"] = "localhost"
    app.config["MAIL_PORT"] = 1025
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = None
    app.config["MAIL_PASSWORD"] = None
    app.config["MAIL_DEFAULT_SENDER"] = "noreply@quiznexus.com"

    mail = Mail(app)
    return mail



def send_email_with_attachment(to_email, subject, body, attachment_data, filename):
    """Send email with CSV attachment"""
    # Configure for MailHog
    smtp_server = "localhost"
    smtp_port = 1025
    smtp_user = "noreply@quiznexus.com"
    smtp_password = None

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment_data.encode())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        # No need for TLS or authentication with MailHog
        # server.starttls()
        # server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
