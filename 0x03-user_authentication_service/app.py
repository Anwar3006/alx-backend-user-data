#!/usr/bin/env python3
"""
FLASK APP with user authentication features.
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Home page
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    Register users
    """
    email_req = request.form['email']
    password_req = request.form['password']

    try:
        AUTH.register_user(email_req, password_req)
        return jsonify(
            {"email": f"{email_req}", "message": "user created"}
        )
    except ValueError:
        return jsonify(
            {"message": "email already registered"}
        ), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Login for users
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    """
    User logout route
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    print(session_id)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    Get user profile based on session_id
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": f"{user.email}"})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Return reset token to be used by user to reset password
    """
    email, password = request.form.get('email'), request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(403)
    token = AUTH.get_reset_password_token(email)
    return jsonify({"email": f"{email}", "reset_token": f"{token}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
