import os
from flask import Flask
from .config import BaseConfig
from .extensions import db, migrate, jwt, sess
from .blueprints import auth_bp, tasks_bp
import redis as redis_lib

def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    # init redis client and attach to app
    app.redis_client = redis_lib.from_url(os.getenv("REDIS_URL"))
    app.config['SESSION_REDIS'] = redis_lib.from_url(os.getenv("SESSION_REDIS_URL"))

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    sess.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    return app