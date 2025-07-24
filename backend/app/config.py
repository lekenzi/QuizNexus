from datetime import timedelta


class Config:
    # Redis
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300

    # Celery
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET_KEY = "your-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    # Flask-Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "your_email@gmail.com"  # Replace with your email
    MAIL_PASSWORD = "your_app_password"  # Replace with your app password
    MAIL_DEFAULT_SENDER = "noreply@example.com"

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///quiznexus.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
