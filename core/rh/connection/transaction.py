"""
"""
from ..session import session


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
            self.create = self.__create
            self.get = self.__get
            self.filter = self.__filter
            self.all = self.__all
            self.update = self.__update
            self.delete = self.__delete

    def __create(self, conn, **kwargs):
        """
        Create a new record in the database.
        """
        # Implement the creation logic here
        pass

    def __get(self, conn, **kwargs):
        """
        Retrieve a single record from the database based on given criteria.
        """
        # Implement the get logic here
        pass

    def __filter(self, conn, **kwargs):
        """
        Retrieve multiple records from the database based on given criteria.
        """
        # Implement the filter logic here
        pass

    def __all(self, conn):
        """
        Retrieve all records from the database.
        """
        # Implement the all logic here
        pass

    def __update(self, conn, **kwargs):
        """
        Update existing records in the database based on given criteria.
        """
        # Implement the update logic here
        pass

    def __delete(self, conn, **kwargs):
        """
        Delete records from the database based on given criteria.
        """
        # Implement the delete logic here
        pass
