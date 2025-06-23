from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class users(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )
    
    