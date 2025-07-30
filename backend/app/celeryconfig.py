from celery.schedules import crontab

beat_schedule = {
    "calculate-ended-quiz-scores": {
        "task": "app.tasks.calculate_ended_quiz_scores",
        "schedule": 10,
    },
    "send-daily-reminders": {
        "task": "app.tasks.send_daily_reminders",
        "schedule": 5,
    },
    "send-monthly-reports": {
        "task": "app.tasks.send_monthly_reports",
        "schedule": crontab(day_of_month=1, hour=9, minute=0),
    },
    # this is for testing
    "test-monthly-reports": {
        "task": "app.tasks.test_monthly_reports",
        "schedule": 30,
    },
}

task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
enable_utc = True
timezone = "UTC"
