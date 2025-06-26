from calendar import c
from datetime import datetime
import re

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.api import api
from app.config import Config
from app.models import db
from werkzeug.security import generate_password_hash
from app.models import User

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
            username="admin",
            password_hash=generate_password_hash("admin_password"),
            full_name=admin_full_name,
            qualification=admin_qualification,
            date_of_birth=admin_date_of_birth,
            is_admin=True,
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

    with app.app_context():
        db.create_all()
        create_super_admin()

    # Register  API resources
    api.init_app(app)

    return app
