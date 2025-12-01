from flask import Blueprint, request, jsonify, current_app, make_response
from ..extensions import db
from ..models.user import User
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt, set_refresh_cookies, unset_jwt_cookies
)
from ..utils.token_store import store_refresh_token, revoke_refresh_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(email=data["email"], username=data["username"])
    user.set_password(data["password"])
    db.session.add(user); db.session.commit()
    return jsonify(user.to_dict()), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Validate fields
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    # Find user
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad credentials"}), 401

    # Create tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    # Get jti from refresh token
    from flask_jwt_extended.utils import get_jti
    jti_refresh = get_jti(refresh_token)

    # Save refresh token in Redis with expiration
    expires = current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
    current_app.redis_client.setex(f"refresh:{jti_refresh}", expires, user.id)

    # Create response
    resp = jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role
        }
    })

    # Send refresh token as HttpOnly secure cookie
    set_refresh_cookies(resp, refresh_token)

    return resp, 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt()["sub"]
    jti = get_jwt()["jti"]
    # check redis if jti exists
    if not current_app.redis_client.get(f"refresh:{jti}"):
        return jsonify({"msg": "Token revoked"}), 401
    new_access = create_access_token(identity=identity)
    return jsonify({"access_token": new_access}), 200

@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt()["jti"]
    current_app.redis_client.delete(f"refresh:{jti}")
    resp = jsonify({"msg": "logged out"})
    unset_jwt_cookies(resp)
    return resp, 200
