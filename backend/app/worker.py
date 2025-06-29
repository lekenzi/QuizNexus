import celery
from celery import Celery
from flask import current_app as app

celery = Celery("Application worker")


class ContextTask(celery.Task):
    """A task that runs in the Flask application context."""

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
