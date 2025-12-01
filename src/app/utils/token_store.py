import uuid
from datetime import datetime, timedelta
import json
from flask import current_app
import redis

REDIS_PREFIX = "refresh_tokens:"

def store_refresh_token(jti: str, user_id: int, expires: int):
    key = f"{REDIS_PREFIX}{jti}"
    r = redis.from_url(current_app.config['SESSION_REDIS'].connection_pool.connection_kwargs['host'])
    # Simpler: use redis client injected in app context; here pseudo
    current_app.redis_client.setex(key, expires, user_id)

def is_refresh_token_revoked(jti: str) -> bool:
    key = f"{REDIS_PREFIX}{jti}"
    return current_app.redis_client.get(key) is None  # if missing -> revoked/expired

def revoke_refresh_token(jti: str):
    key = f"{REDIS_PREFIX}{jti}"
    current_app.redis_client.delete(key)
