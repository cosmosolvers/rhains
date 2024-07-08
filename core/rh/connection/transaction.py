"""
"""
from ..session import session
from ..result.scalar import Scalar, Matrix

from exceptions.core.rh import database as db


class Transaction:
    def __init__(self, model, connexion) -> None:
        self.__model = model
        self.__connexion = connexion

    def atomic(self):
        """
        This method is intended to be used as a context manager for 
        managing database transactions atomically.
        """
        with session(self.__connexion) as conn:
            self.create = lambda **kwargs: self.__create(conn, **kwargs)
            self.get = lambda **kwargs: self.__get(conn, **kwargs)
            self.filter = lambda **kwargs: self.__filter(conn, **kwargs)
            self.all = lambda: self.__all(conn)
            self.update = lambda **kwargs: self.__update(conn, **kwargs)
            self.delete = lambda **kwargs: self.__delete(conn, **kwargs)

    def __create(self, conn, **kwargs) -> Scalar:
        """
        Create a new record in the database.
        """
        try:
            pass
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)

    def __get(self, conn, **kwargs) -> Scalar | None:
        """
        Retrieve a single record from the database based on given criteria.
        """
        try:
            pass
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)

    def __filter(self, conn, **kwargs) -> Matrix | list:
        """
        Retrieve multiple records from the database based on given criteria.
        """
        try:
            pass
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)

    def __all(self, conn) -> Matrix | None:
        """
        Retrieve all records from the database.
        """
        try:
            pass
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)

    def __update(self, conn, **kwargs) -> Scalar | None:
        """
        Update existing records in the database based on given criteria.
        """
        try:
            pass
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)

    def __delete(self, conn, **kwargs) -> bool:
        """
        Delete records from the database based on given criteria.
        """
        try:
            pass
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)
