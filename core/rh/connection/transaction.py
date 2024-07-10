"""
"""
from utils.data import instance as _
from utils.data import treatment

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
            self.__validated_data(**kwargs)
            _(self, kwargs.values())
            instance = self.__model(**kwargs)
            instance_fields = instance.__to_dict()
            result = self.__connexion.bulk_create(
                conn, self.__model.__name__.lower(), **instance_fields)
            if not result:
                raise db.DataBaseCreateError('create failed')

            instance = self.__model(**result)
            return Scalar(instance, self)
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)

    def __get(self, conn, **kwargs) -> Scalar | None:
        """
        Retrieve a single record from the database based on given criteria.
        """
        try:
            self.__validated_data(**kwargs)
            if '$pk' not in kwargs.keys():
                raise db.RequestParamsError('pk field required')

            _(self, kwargs.values())
            result = self.__connexion.bulk_get(self.__model.__name__.lower(), **kwargs.get('$pk'))
            del kwargs['$pk']

            if not result:
                return None

            result = self.__model(**result)
            if not result or not treatment(result, kwargs):
                return None

            return Scalar(result, self)
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)

    def __filter(self, conn, **kwargs) -> Matrix | list:
        """
        Retrieve multiple records from the database based on given criteria.
        """
        try:
            self.__validated_data(**kwargs)
            data = {}
            for k, v in kwargs.items():
                if isinstance(v, dict):
                    data[k] = v
                    del kwargs[k]

            result = self.__connexion.bulk_filter(self.__model.__name__.lower(), **kwargs)
            if not result:
                return []
            result = [self.__model(**item) for item in result]
            # treatment
            if len(result) <= 0 or not treatment(result, data):
                return []

            return Matrix(result, self)
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)

    def __all(self, conn) -> Matrix | None:
        """
        Retrieve all records from the database.
        """
        try:
            result = self.__connexion.bulk_all(self.__model.__name__.lower())
            if not result:
                return None
            result = [self.__model(**item) for item in result]
            return Matrix(result, self)
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)

    def __update(self, conn, **kwargs) -> Scalar | None:
        """
        Update existing records in the database based on given criteria.
        """
        try:
            self.__validated_data(**kwargs)
            data = {}
            if '$commit' not in kwargs:
                raise db.DataBaseConditionError('missing $commit')
            data['$commit'] = kwargs['$commit']
            del kwargs['$commit']

            if '$pk' not in kwargs.keys():
                raise db.RequestParamsError('pk field required')
            data['$pk'] = kwargs['$pk']
            result = self.get(kwargs.get('$pk'))
            del kwargs['$pk']

            if not result or treatment(result, kwargs):
                return None

            result = self.__connexion.bulk_update(self.__model.__name__.lower(), **data)
            if not result:
                return None

            return self.get(kwargs.get('$pk'))
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)

    def __delete(self, conn, **kwargs) -> bool:
        """
        Delete records from the database based on given criteria.
        """
        try:
            self.__validated_data(**kwargs)
            if '$pk' not in kwargs.keys():
                raise db.RequestParamsError('pk field required')

            result = self.get(kwargs.get('$pk'))
            if not result or not treatment(result, kwargs):
                return False

            result = self.__connexion.delete(
                self.__model.__name__.lower(),
                **{'$pk': kwargs.get('$pk')}
            )
            return result
        except Exception as e:
            conn.rollback()
            raise db.DatabaseError(e)
