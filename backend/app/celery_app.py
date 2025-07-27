from app.config import Config
from celery import Celery

celery_app = Celery("tasks", backend=Config.CELERY_RESULT_BACKEND, broker=Config.CELERY_BROKER_URL)

# Import tasks to ensure they are registered with Celery
import app.tasks