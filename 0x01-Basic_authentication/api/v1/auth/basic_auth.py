#!/usr/bin/env python3
"""Baic Auth class
"""
from .auth import Auth
import re
import base64
import binascii


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
        type(base64_authorization_header) != str:
            return None
        try:
            res = base64.b64decode(
                base64_authorization_header,
                validate=True,
            )
            return res.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None
