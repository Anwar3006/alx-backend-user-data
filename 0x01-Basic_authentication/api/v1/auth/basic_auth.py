#!/usr/bin/env python3
"""Baic Auth class
"""
from .auth import Auth
import re
import base64
import binascii
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Basic authentication class.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None or\
                not isinstance(authorization_header, str) or\
                authorization_header.startswith('Basic ') is False:
            return None
        else:
            split = re.split("Basic\\s", authorization_header)
            for i in split[1:]:
                return i

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            res = base64.b64decode(
                base64_authorization_header,
                validate=True,
            )
            return res.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Returns the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str) or\
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        split = re.split(":", decoded_base64_authorization_header)
        return (split[0], split[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password.
        """
        if not isinstance(user_email, str) and not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if len(users) <= 0:
            return None
        else:
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None
