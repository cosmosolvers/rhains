"""

"""
from utils.data import instance as _
from utils.data import treatment

from ..result.scalar import Scalar, Matrix

from exceptions.core.rh import database as db


class Collection:
    def __init__(self, model, connexion) -> None:
        self.__model = model
        self.__connexion = connexion

    def __validated_data(self, **kwargs) -> dict:
        if len(kwargs) == 0:
            raise db.DatabaseParamsError("data can't be empty")

    def atomic(self, *args) -> bool:
        """
        COLLECT
        =======

        many syntax
        -----------
        [
            {
                '$set': {
                }
            },
            {
                '$push': {
                }
            },
            ...
        ]
        """
        if len(args) <= 0:
            raise db.DatabaseParamsError("params can't empty")
        result = self.__connexion.collect(self, *args)
        return result

    # $push
    def create(self, **kwargs) -> Scalar:
        """
        CREATE
        ======

        create syntax
        -------------
        {
            'field': 'value',
            'field': 'value',
            'field': User()
            ...
        }
        """
        self.__validated_data(**kwargs)
        _(self, kwargs.values())
        instance = self.__model(**kwargs)
        instance_fields = instance.__to_dict()
        result = self.__connexion.create(self.__model.__name__.lower(), **instance_fields)
        if not result:
            raise db.DataBaseCreateError('create failed')

        instance = self.__model(**result)
        return Scalar(instance, self)

    # $get
    def get(self, **kwargs) -> Scalar | None:
        """
        GET
        ===

        get syntax
        -----------
        {
            '$pk': {
                'field': value
            },
            'field': 'value',
            'field': 'value',
            ...
        }
        """
        self.__validated_data(**kwargs)
        if '$pk' not in kwargs.keys():
            raise db.RequestParamsError('pk field required')

        _(self, kwargs.values())
        result = self.__connexion.get(self.__model.__name__.lower(), **kwargs.get('$pk'))
        del kwargs['$pk']

        if not result:
            return None

        result = self.__model(**result)
        if not result or not treatment(result, kwargs):
            return None

        return Scalar(result, self)

    def filter(self, **kwargs) -> Matrix | list:
        """
        FILTER
        ======

        filter syntax
        -------------
        {
            'field': 'value',
            'field': 'value',
            ...
        }
        """
        self.__validated_data(**kwargs)
        data = {}
        for k, v in kwargs.items():
            if isinstance(v, dict):
                data[k] = v
                del kwargs[k]

        result = self.__connexion.filter(self.__model.__name__.lower(), **kwargs)
        if not result:
            return []
        result = [self.__model(**item) for item in result]
        # treatment
        if len(result) <= 0 or not treatment(result, data):
            return []

        return Matrix(result, self)

    def all(self) -> Matrix | None:
        """
        ALL
        ===
        """
        result = self.__connexion.all(self.__model.__name__.lower())
        if not result:
            return None
        result = [self.__model(**item) for item in result]
        return Matrix(result, self)

    # $set
    def update(self, **kwargs) -> Scalar | None:
        """
        UPDATE
        ======

        update syntax
        -------------
        {
            '$pk': {'field': value},
            'field': 'value',
            'field': 'value',
            ...,
            '$commit': {
                'field': 'value',
                'field': 'value',
                ...,
            }
        }
        """
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

        result = self.__connexion.update(self.__model.__name__.lower(), **data)
        if not result:
            return None

        return self.get(kwargs.get('$pk'))

    # $del
    def delete(self, **kwargs) -> bool:
        """
        DELETE
        ======

        delete syntax
        -------------
        {
            '$pk': {'field': value},
            'field': 'value',
            'field': 'value',
            ...
        }
        """
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

    # create table if does'nt exists
    def table(self) -> str:
        return self.__connexion.table(self.__model)

    # mis a jour de la table
    def alter(self):
        self.__connexion.alter(self.__model)
