from celery import Celery

from app.config import Config

celery_app = Celery(
    "tasks", backend=Config.CELERY_RESULT_BACKEND, broker=Config.CELERY_BROKER_URL
)


celery_app.config_from_object("app.celeryconfig")
