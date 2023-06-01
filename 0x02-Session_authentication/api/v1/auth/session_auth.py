#!/usr/bin/env python3
"""
Session Authentication
"""
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    Session Auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        self.id = str(uuid4())
        self.user_id_by_session_id[self.id] = user_id
        return self.id
