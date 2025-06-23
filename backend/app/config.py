from datetime import timedelta


class Config:
    CACHE_TYPE = "RedisCache"
    JWT_SECRET_KEY = "i_dont_like_java"
    CACHE_REDIS_HOST = "localhost"
    SQLALCHEMY_DATABASE_URI = "sqlite:///quiznexus.sqlite3"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    CACHE_REDIS_PORT = 6379
    SECRET_KEY = "this_is_a_top_secret"
    CACHE_DEFAULT_TIMEOUT = 300
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=4)
    DEBUG = True
