#!/usr/bin/env python3
"""
FLASK APP
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
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
    email_req = request.form['email']
    password_req = request.form['password']

    if not AUTH.valid_login(email_req, password_req):
        abort(401)
    sessionID = AUTH.create_session(email_req)

    return jsonify(
        {"email": f"{email_req}",
         "message": "logged in"}).set_cookie('session_id', sessionID)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
