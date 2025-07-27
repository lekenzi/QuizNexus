from celery.schedules import crontab

beat_schedule = {
    # Check more frequently (every 15 seconds)
    "check-exams-frequently": {
        "task": "app.tasks.check_and_start_exams",
        "schedule": 15.0,
    },
}

task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
enable_utc = True
timezone = "UTC"
task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
enable_utc = True
timezone = "UTC"
