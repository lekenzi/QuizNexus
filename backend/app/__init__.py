from datetime import datetime

import yaml
from flask import Flask, Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

from app import worker
from app.api import api
from app.cache import redis_client
from app.config import Config
from app.email import configure_mail
from app.models import User, db
from app.worker import configure_celery

celery = None


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

    
    db.init_app(app)

    
    migrate = Migrate(app, db)

    JWTManager(app)
    CORS(app)

    global celery
    celery = configure_celery(app)

    with app.app_context():
        redis_client.ping()
        print("Redis connected successfully!")

        db.create_all()
        create_super_admin()

    configure_mail(app)

    api.init_app(app)

    return app
