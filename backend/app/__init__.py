from datetime import datetime

from app import worker
from app.api import api
from app.config import Config
from app.models import User, db
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash


def create_super_admin():

    admin_username = "admin"
    admin_user = User.query.filter_by(username=admin_username).first()
    admin_full_name = "Admin"
    admin_qualification = "Admin"
    admin_date_of_birth = datetime(
        year=1990, month=1, day=1, hour=0, minute=0, second=0
    )
    if not admin_user:
        admin = User(
            username=admin_username,
            password_hash=generate_password_hash("admin"),
            full_name=admin_full_name,
            qualification=admin_qualification,
            date_of_birth=admin_date_of_birth,
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists!")


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    celery = worker.celery
    celery.conf.update(
        broker=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery = worker.celery
    celery.conf.update(
        broker=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        task_serializer="json",
    )

    celery.autodiscover_tasks(["tasks"])
    celery.Task = worker.ContextTask

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

    # Register  API resources
    api.init_app(app)

    @app.route("/")
    def index():
        return "Welcome to the backend!"

    return app
