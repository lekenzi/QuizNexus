from celery.schedules import crontab

beat_schedule = {
    "calculate-ended-quiz-scores": {
        "task": "app.tasks.calculate_ended_quiz_scores",
        "schedule": 3600,
    },
}

task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
enable_utc = True
timezone = "UTC"
