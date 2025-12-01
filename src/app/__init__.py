import os
from flask import Flask
from .config import BaseConfig
from .extensions import db, migrate, jwt, sess
from .blueprints import auth_bp, tasks_bp
import redis as redis_lib
from .utils.fake_redis import FakeRedis

def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    if testing:
        app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "JWT_COOKIE_SECURE": False,
            "JWT_TOKEN_LOCATION": ["headers", "cookies"],
            "SESSION_REDIS": None,
        })
        app.redis_client = FakeRedis()

    else:
        redis_url = os.getenv("REDIS_URL")
        session_redis_url = os.getenv("SESSION_REDIS_URL")

        app.redis_client = redis_lib.from_url(redis_url)
        app.config["SESSION_REDIS"] = redis_lib.from_url(session_redis_url)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    sess.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    return app
