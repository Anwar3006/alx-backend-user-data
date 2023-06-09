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
from typing import Union


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
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Returns user based on session_id
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Updates the corresponding user’s session ID to None.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a UUID and update the user’s reset_token database field
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError
        get_uuid = _generate_uuid()
        self._db.update_user(user.id, reset_token=get_uuid)
        return get_uuid

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update password of user using reset_token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        if user is None:
            raise ValueError
        hashed = _hash_password(password)
        self._db.update_user(user.id, reset_token=None, hashed_password=hashed)
