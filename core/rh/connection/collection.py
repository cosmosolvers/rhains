"""

"""
from typing import Tuple, Optional, Union

from utils.data import instance as _
from utils.data import foreignkeys

from ..result.scalar import Scalar, Matrix

from exceptions.core.rh import database as db


class Collection:
    def __init__(self, model, connexion) -> None:
        self.__model = model
        self.__connexion = connexion

    def __validated_data(self, **kwargs) -> dict:
        if len(kwargs) == 0:
            raise db.DatabaseParamsError("data can't be empty")

    def collect(self, **kwargs) -> Optional[Tuple[Union[Scalar, Matrix]]]:
        """
        COLLECT
        =======

        many syntax
        -----------
        {
            '$': [
                {
                    '$get': {
                    }
                },
                {
                    '$get': {
                    }
                },
                ...
            ]
        }
        """
        self.__validated_data(**kwargs)
        args = []
        key, value = kwargs.popitem()
        if key != '$':
            raise db.DatabaseRequestError("`$` only")
        if not isinstance(value, list):
            raise db.DatabaseParamsError(f"{value} must be list")
        if len(value) == 0:
            raise db.DatabaseValueError(f"{value} can't be free")
        if not all(type(item) is dict for item in value):
            raise db.DatabaseValueItemError("data item invalid")

        for item in value:
            k, v = item.popitem()
            match k:
                # get
                case '$get': args.append(self.get(**v))
                case '$pull': args.append(self.create(**v))
                # update
                case '$set': args.append(self.update(**v))
                # delete
                case '$del': args.append(self.delete(**v))
                # create
                case '$push': args.append(self.create(**v))
        return tuple(args)

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

        data = kwargs['$pk']
        del kwargs['$pk']

        _(self, kwargs.values())
        result = self.__connexion.get(self.__model.__name__.lower(), **data)
        if not result:
            return None
        elif isinstance(result, dict):
            result = self.__model(**result)
            # treatment
            return Scalar(result, self)
        else:
            raise db.DataBaseConditionError('too many results')

    def filter(self, **kwargs) -> Matrix | None:
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
        for k, v in kwargs.items():
            if isinstance(v, dict):
                data[k] = v
                del kwargs[k]

        result = self.__connexion.filter(self.__model.__name__.lower(), **kwargs)
        if not result:
            return None
        result = [self.__model(**item) for item in result]
        # treatment
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
    def update(self, **kwargs) -> Matrix | Scalar | None:
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
        del kwargs['$pk']

        result = self.__connexion.update(self.__model.__name__.lower(), **data)
        if not result:
            return None
        if isinstance(result, dict):
            result = self.__model(**result)
            # treatment
            return Scalar(result, self)
        else:
            return Matrix([self.__model(**item) for item in result])

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

        result = self.get({'$pk': kwargs.get('$pk')})
        # treatment
        result = self.__connexion.delete(
            self.__model.__name__.lower(),
            **{'$pk': kwargs.get('$pk')}
        )
        if not result:
            raise db.DataBaseDeleteError('delete failed')
        return True

    # create table if does'nt exists
    def table(self) -> str:
        return self.__connexion.table(self.__model)

    # mis a jour de la table
    def alter(self):
        self.__connexion.alter(self.__model)
