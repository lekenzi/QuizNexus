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

    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = "noreply@example.com"


def configure_mail(app):
    """Configure Flask-Mail"""
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "your_email@gmail.com"  
    app.config["MAIL_PASSWORD"] = "your_app_password"  
    app.config["MAIL_DEFAULT_SENDER"] = "noreply@example.com"

    mail = Mail(app)
    return mail


class EmailService:
    """Email service class for sending various types of emails"""

    def __init__(self, mail_instance=None):
        self.mail = mail_instance

    def send_simple_email(self, to_email, subject, body):
        """Send simple text email"""
        try:
            msg = Message(
                subject=subject,
                recipients=[to_email],
                body=body,
                sender=EmailConfig.MAIL_DEFAULT_SENDER,
            )
            self.mail.send(msg)
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

    def send_html_email(self, to_email, subject, html_body):
        """Send HTML email"""
        try:
            msg = Message(
                subject=subject,
                recipients=[to_email],
                html=html_body,
                sender=EmailConfig.MAIL_DEFAULT_SENDER,
            )
            self.mail.send(msg)
            return True
        except Exception as e:
            print(f"HTML email sending failed: {e}")
            return False

    def send_quiz_reminder(self, user_email, user_name, quiz_count):
        """Send quiz reminder email"""
        subject = "🎯 Quiz Reminder - New Quizzes Available!"

        html_body = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .button {{ background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Quiz Master</h1>
                    </div>
                    <div class="content">
                        <h2>Hi {user_name}!</h2>
                        <p>You have <strong>{quiz_count} new quizzes</strong> available to attempt.</p>
                        <p>Don't miss out on improving your knowledge!</p>
                        <br>
                        <p>Visit your dashboard to start learning:</p>
                        <a href="http://localhost:5000/dashboard" class="button">Go to Dashboard</a>
                        <br><br>
                        <p>Best regards,<br>Quiz Master Team</p>
                    </div>
                </div>
            </body>
        </html>
        """

        return self.send_html_email(to_email, subject, html_body)

    def send_monthly_report(self, user_email, user_name, report_data):
        """Send monthly performance report"""
        subject = f"📊 Monthly Performance Report - {user_name}"

        html_body = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #2196F3; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                    .stat-box {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; text-align: center; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Monthly Performance Report</h1>
                        <p>{user_name}</p>
                    </div>
                    <div class="content">
                        <div class="stats">
                            <div class="stat-box">
                                <h3>{report_data.get('total_quizzes', 0)}</h3>
                                <p>Total Quizzes</p>
                            </div>
                            <div class="stat-box">
                                <h3>{report_data.get('average_score', 0):.1f}%</h3>
                                <p>Average Score</p>
                            </div>
                            <div class="stat-box">
                                <h3>{report_data.get('total_score', 0)}</h3>
                                <p>Total Points</p>
                            </div>
                        </div>
                        
                        <h3>Recent Quiz Attempts:</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Quiz</th>
                                    <th>Date</th>
                                    <th>Score</th>
                                    <th>Performance</th>
                                </tr>
                            </thead>
                            <tbody>
        """

        for attempt in report_data.get("recent_attempts", []):
            performance = (
                "Excellent"
                if attempt["score"] >= 80
                else "Good" if attempt["score"] >= 60 else "Needs Improvement"
            )
            html_body += f"""
                                <tr>
                                    <td>{attempt['quiz_name']}</td>
                                    <td>{attempt['date']}</td>
                                    <td>{attempt['score']}%</td>
                                    <td>{performance}</td>
                                </tr>
            """

        html_body += """
                            </tbody>
                        </table>
                        
                        <p>Keep up the great work! 🎉</p>
                        <p>Best regards,<br>Quiz Master Team</p>
                    </div>
                </div>
            </body>
        </html>
        """

        return self.send_html_email(user_email, subject, html_body)

    def send_csv_export_notification(self, user_email, user_name, download_link=None):
        """Send CSV export completion notification"""
        subject = "📄 Your Quiz Data Export is Ready!"

        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2>Hi {user_name}!</h2>
                    <p>Your quiz data export has been completed successfully.</p>
                    <p>The CSV file contains all your quiz attempts and scores.</p>
                    
                    {"<p><a href='" + download_link + "' style='background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>Download CSV</a></p>" if download_link else "<p>The CSV file has been sent as an attachment.</p>"}
                    
                    <p>Best regards,<br>Quiz Master Team</p>
                </div>
            </body>
        </html>
        """

        return self.send_html_email(user_email, subject, html_body)


def send_email(to_email, subject, body, is_html=False):
    """Send email using SMTP"""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "your_email@gmail.com"  
    smtp_password = "your_app_password"  

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    if is_html:
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


def send_email_with_attachment(to_email, subject, body, attachment_data, filename):
    """Send email with CSV attachment"""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "your_email@gmail.com"  
    smtp_password = "your_app_password"  

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment_data.encode())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {filename}'
    )
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
