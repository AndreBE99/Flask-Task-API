import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY") or "dev"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "jwt-secret"
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 900))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 2592000))
    SESSION_TYPE = os.getenv("SESSION_TYPE", "redis")
    SESSION_REDIS = None