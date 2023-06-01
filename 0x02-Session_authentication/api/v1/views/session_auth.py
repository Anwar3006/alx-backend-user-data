#!/usr/bin/env python3
"""
View for Session Authentication
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from .users import User
from os import getenv
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
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
        return jsonify({"error": "no user found for this email"}), 404

    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    if users[0].is_valid_password(user_pwd) is False:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(getattr(users[0], 'id'))
    response = jsonify(users[0].to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response

@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Return:
      - An empty JSON object.
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})
