#!/usr/bin/env python3
"""Baic Auth class
"""
from auth import Auth
import re


class BasicAuth(Auth):
    """
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None or\
                not isinstance(authorization_header, str) or\
                authorization_header.startswith('Basic ') == False:
            return None
        else:
            split = re.split("Basic\\s", authorization_header)
            for i in split[1:]:
                return i
