import csv
import io
import smtplib
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from app.email import send_email, send_email_with_attachment
from celery import current_app
from flask_mail import Message
from models import Quiz, Score, User


@current_app.task(bind=True)
def send_daily_reminders(self):
    """Send daily quiz reminders to users"""
    try:
        users = User.query.all()
        new_quizzes = Quiz.query.filter(
            Quiz.date_of_quiz >= datetime.now().date()
        ).all()

        for user in users:

            recent_attempts = (
                Score.query.filter_by(user_id=user.id)
                .filter(
                    Score.time_stamp_of_attempt >= datetime.now() - timedelta(days=1)
                )
                .count()
            )

            if recent_attempts == 0 and new_quizzes:
                send_reminder_email.delay(user.id, len(new_quizzes))

        return f"Sent reminders to {len(users)} users"
    except Exception as e:
        self.retry(countdown=60, max_retries=3)


@current_app.task(bind=True)
def send_monthly_reports(self):
    """Generate and send monthly performance reports"""
    try:
        users = User.query.all()
        for user in users:
            generate_monthly_report.delay(user.id)
        return f"Generated reports for {len(users)} users"
    except Exception as e:
        self.retry(countdown=60, max_retries=3)


@current_app.task
def send_reminder_email(user_id, quiz_count):
    """Send email reminder to specific user"""
    user = User.query.get(user_id)
    if not user:
        return "User not found"

    subject = "Quiz Reminder - New Quizzes Available!"
    body = f"""
    Hi {user.full_name},
    
    You have {quiz_count} new quizzes available to attempt.
    Visit your dashboard to start learning!
    
    Best regards,
    Quiz Master Team
    """

    send_email(user.username, subject, body)
    return f"Reminder sent to {user.username}"


@current_app.task
def generate_monthly_report(user_id):
    """Generate monthly performance report for user"""
    user = User.query.get(user_id)
    if not user:
        return "User not found"

    last_month = datetime.now() - timedelta(days=30)
    scores = (
        Score.query.filter_by(user_id=user.id)
        .filter(Score.time_stamp_of_attempt >= last_month)
        .all()
    )

    if not scores:
        return "No quiz attempts in last month"

    total_quizzes = len(scores)
    total_score = sum(score.total_scored for score in scores)
    average_score = total_score / total_quizzes if total_quizzes > 0 else 0

    html_report = f"""
    <html>
    <head><title>Monthly Performance Report</title></head>
    <body>
        <h2>Monthly Performance Report - {user.full_name}</h2>
        <p><strong>Period:</strong> {last_month.strftime('%B %Y')}</p>
        <p><strong>Total Quizzes Attempted:</strong> {total_quizzes}</p>
        <p><strong>Total Score:</strong> {total_score}</p>
        <p><strong>Average Score:</strong> {average_score:.2f}</p>
        <hr>
        <h3>Quiz Details:</h3>
        <table border="1" style="border-collapse: collapse;">
            <tr>
                <th>Quiz ID</th>
                <th>Date</th>
                <th>Score</th>
            </tr>
    """

    for score in scores:
        html_report += f"""
            <tr>
                <td>{score.quiz_id}</td>
                <td>{score.time_stamp_of_attempt.strftime('%Y-%m-%d')}</td>
                <td>{score.total_scored}</td>
            </tr>
        """

    html_report += """
        </table>
    </body>
    </html>
    """

    send_email(user.username, "Monthly Performance Report", html_report, is_html=True)
    return f"Monthly report sent to {user.username}"


@current_app.task
def export_quiz_data_csv(user_id):
    """Export user's quiz data to CSV"""
    user = User.query.get(user_id)
    if not user:
        return "User not found"

    scores = Score.query.filter_by(user_id=user.id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Quiz ID", "Chapter ID", "Date", "Score", "Remarks"])

    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        writer.writerow(
            [
                score.quiz_id,
                quiz.chapter_id if quiz else "N/A",
                score.time_stamp_of_attempt.strftime("%Y-%m-%d"),
                score.total_scored,
                "Quiz completed",
            ]
        )

    csv_data = output.getvalue()
    send_email_with_attachment(
        user.username,
        "Quiz Data Export",
        "Please find your quiz data attached.",
        csv_data,
        "quiz_data.csv",
    )

    return f"CSV export sent to {user.username}"
