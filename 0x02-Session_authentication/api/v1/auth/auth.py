#!/usr/bin/env python3
"""Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    create a class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Define which routes don't need authentication
        Returns True if the path is not in excluded_paths
        """
        if path is None or excluded_paths is None or\
                len(excluded_paths) == 0:
            return True

        if path + '/' in excluded_paths or path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        Request validation!
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request.
        """
        return None
    
    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        """
        if request:
            return request.cookies.get('_my_session_id')
        return None
