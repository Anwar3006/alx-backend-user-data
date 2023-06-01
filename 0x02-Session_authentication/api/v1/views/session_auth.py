#!/usr/bin/env python3
"""
View for Session Authentication
"""
from flask import jsonify, request
from api.v1.views import app_views
from .users import User
from os import getenv


@app_views.route('/auth_session/login', method=['POST'], strict_slashes=False)
def handle_session_auth() -> str:
    """POST /auth_session/login
    Handles all routes for the Session authentication.
    """
    user_email = request.form.get('email')
    if not user_email:
        return jsonify({"error": "email missing"}), 400

    user_pwd = request.form.get('password')
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': user_email})
    except Exception:
        if len(users) <= 0:
            return jsonify({"error": "no user found for this email"}), 404

    if users[0].is_valid_password(user_pwd) is False:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(getattr(users[0], 'id'))
    response = jsonify(users[0].to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response
