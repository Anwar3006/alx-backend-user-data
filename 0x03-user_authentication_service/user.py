#!/usr/bin/env python3
"""
User model
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
    Create Schema for users
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __init__(
            self,
            email: str,
            hashed_password: str,
            session_id: str = None,
            reset_token: str = None):
        """
        Initialize class
        """
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = session_id
        self.reset_token = reset_token

    def __repr__(self):
        """Return String Representation of Objects"""
        return 'User with <{}> has password <{}>'\
            .format(self.email, self.hashed_password)
