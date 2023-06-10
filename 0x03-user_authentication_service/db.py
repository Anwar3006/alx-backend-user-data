#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add user to DB
        """
        try:
            user = User(email, hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Returns the first row found in the users table
        """
        field = []
        values = []
        for k, v in kwargs.items():
            if not hasattr(User, k):
                raise InvalidRequestError()
            else:
                field.append(getattr(User, k))
                values.append(v)
        result = self._session.query(User).filter(
            tuple_(*field).in_([tuple(values)])).first()
        if result:
            return result
        else:
            raise NoResultFound()

    def update_user(self, user_id: str, **kwargs) -> None:
        """
        Updates the user by user_id
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        fields_to_update = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields_to_update[getattr(User, key)] = value
            else:
                raise ValueError
        self.__session.query(User).filter(User.id == user_id).update(
            fields_to_update,
            synchronize_session=False
        )
        self._session.commit()
