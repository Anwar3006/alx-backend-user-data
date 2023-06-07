#!/usr/bin/env python3
"""
User Authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string arguments and returns bytes.
    """
    if not isinstance(password, str):
        return None
    encode_to_byte = password.encode('utf8')
    hash_pwd = bcrypt.hashpw(encode_to_byte, bcrypt.gensalt())
    return hash_pwd


def _generate_uuid() -> str:
    """
    Return a string representation of a new UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register users' credentials to DB
        """
        # get user by passing email to DB.find_user_by(email=email)
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hash_pwd = _hash_password(password)
            return self._db.add_user(email, hash_pwd)
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Credentials validation
        """
        try:
            get_user = self._db.find_user_by(email=email)
            passwd = password.encode('utf-8')
            return bcrypt.checkpw(passwd, get_user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Returns the session ID
        """
        try:
            get_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(get_user.id, session_id=session_id)
        return session_id
