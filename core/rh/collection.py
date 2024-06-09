"""
ENCAPSULATION DES DONNEES
=========================

primary syntax
--------------
create : '$push'
list   : '$pull'
get    : '$get'
update : '$set'
delete : '$del'

create syntax
-------------
{
    '$push': {
        'field': 'value',
        'field': 'value',
        ...
    }
}

get syntax
----------
1. simple get
{
    '$get': {
        'field': 'value',
        'field': 'value',
    }
}
2. get with primary condition
{
    '$get': {
        'field': 'value',
        'field1': {'$lt': 'value'}
    }
}
3. get with foreign key
{
    '$get': {
        'field': 'value',
        # lorsque vous voulez mettre une condition sur un/plusieurs
        # champ de la table associer a la fk
        'field1': {
            'field': 'value',
            ...
            }
        }
    }
}

list syntax
-----------
1. simple list
{
    '$pull': {'$': '*'}
}
2. filter
{
    '$pull': {
        'field': 'value',
        'field': {'$gt': 'value'}
    }
}
3. utiliser les requirements
{
    '$pull': {
        'field': 'value',
        'field': {
            'field': value,
            'field': value
        }
    }
}
4. utiliser les agents
{
    '$pull': {
        'field': 'value',
        'field': {'$gt': 'value'}
        '$': [
            {'$-': {'field': 'value'}},
            {'$.': '!'}
        ]
    }
}
5. utiliser les conditions
{
    '$pull': {
        'field': 'value',
        'field': {'$gt': 'value'}
        'field': {'$lt': 'value'},
        'field': {'$le': 'value'},
        'field': {'$gt': 'value'},
        'field': {'$ge': 'value'},
        'field': {'$in': 'value'},
        'field': {'$nin': 'value'},
        'field': {'$ne': 'value'},
        'field': {'$like': 'value'},
        'field': {'$min': 'value'},
        'field': {'$max': 'value'},
        'field': {'$avg': 'value'},
        'field': {'$rm': 'value'},
        'field': {'$add': 'value'},
        'field': {'$set': 'value'}
        }
    }
}

update syntax
-------------
{
    '$set': {
        'field': 'value',
        'field': 'value',
        ...,
        '$commit': {
            'field': 'value',
            'field': 'value',
        }
    }
}

delete syntax
-------------
{
    '$del': {
        'field': 'value',
        'field': 'value',
        ...
    }
}

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
    ]
}

the agents
----------
s'appliquent uniquement sur un pull

1. all
    {'$.': '*'}
2. exists
    {'$.': '!'}
3. count
    {'$.': '?'}
4. sort
    {'$sort': 'field'}
5. limit
    {'$.': (0, n)}
6. exclude
    {'$-': {'field': 'value'}}
8. first
    {'$.': 0}
9. last
    {'$.': -1}

the conditions
--------------
s'appliquent uniquement sur les champs

1. less than
    {'$lt: value}
2. less than or equal
    {'$le': value}
3. greater than
    {'$gt': value}
4. greater than or equal
    {'$ge': value}
5. in
    {'$in': value}
6. not in
    {'$nin': value}
7. not equal
    {'$ne': value}
8. like
    {'$like': value}
9. between
    {'$$': (n, m)}
10. min
    {'$min': value}
11. max
    {'$max': value}
12. avg
    {'$avg': value}
4. partial
    {'$rm': value} / {'$add': value}

the keys
--------
1. many
    {'$': {} }
    
2. atomic
    {'$atomic': True} default False
the meta
--------
1. aggregation
    {'$agg': {'field': 'value'}}
"""
from exception.core.rh.database import collection as db

from .database import (
    SqliteCRUD,
    PostgresCRUD,
    MysqlCRUD,
    MongoDBCRUD,
    ArangoDBCRUD
)
from .result.scalar import Scalar, Matrix

instruct = {
    'sqlite': SqliteCRUD,
    'mysql': MysqlCRUD,
    'postgres': PostgresCRUD,
    'mongodb': MongoDBCRUD,
    'Arangodb': ArangoDBCRUD
}


class Connection:
    def __init__(self, **kwargs) -> None:
        self.__connexion = instruct.get(kwargs.get('engine'))(kwargs.get('connect'))
        self.__model = kwargs.get('model')
        self.tablename = str(self.__model.__name__).lower()

    @property
    def collection(self):
        return Collection(self.__model, self.__connexion)


class Collection:
    def __init__(self, model, connexion) -> None:
        self.__model = model
        self.__connexion = connexion

    def collect(self, method: str, **kwargs):
        if method not in ('$get', '$set', '$del', '$push', '$pull', '$'):
            raise db.DataBaseRequestNotFoundError(f"{method} not allowed")
        if kwargs:
            if len(kwargs) != 1:
                raise db.DataBaseConditionError('too many arguments')
            key, value = kwargs.popitem()
            match key:
                case '$get': return self.get(**value)
                case '$set': return self.update(**value)
                case '$del': return self.delete(**value)
                case '$push': return self.create(**value)
                case '$pull': return self.filter(**value)
                case '$':
                    if not isinstance(value, list):
                        raise db.DataBaseFieldTypeError(f"{value} must be list")
                    args = []
                    for val in value:
                        args.append(self.collect(**val))
                    return tuple(args)
        return self._all()

    # $push
    def create(self, **kwargs) -> Scalar:
        """
        kwargs: {
            'field': 'value',
            'field': 'value',
            ...
        }
        """
        instance = self.__model(**kwargs)
        instance_fields = instance.__to_dict()
        result = self.__connexion.create(self._model.__name__, **instance_fields)
        instance = self.__model(**result)
        return Scalar(instance, self)

    def all(self, **kwargs) -> Matrix | None:
        result = self.__connexion.all(self._model.__name__)
        return Matrix(self, *[self._model(**item) for item in result]) if result else None

    def filter(self, **kwargs) -> Matrix | None:
        """
        kwargs: {
            'field': 'value',
            'field': 'value',
            ...
        }
        """
        result = self.__connexion.filter(self._model.__name__, **kwargs)
        return Matrix(self, *[self._model(**item) for item in result]) if result else None

    def get(self, **kwargs) -> Scalar | None:
        """
        kwargs: {
            'field': 'value',
            'field': 'value',
            ...
        }
        """
        result = self.__connexion.get(self._model.__name__, **kwargs)
        if not result:
            return None
        if isinstance(result, dict):
            return Scalar(self._model(**result), self)
        else:
            raise db.DataBaseConditionError('too many results')

    def update(self, **kwargs) -> Matrix | Scalar | None:
        """
        kwargs: {
            'field': 'value',
            'field': 'value',
            ...,
            '$commit': {
                'field': 'value',
                'field': 'value',
            }
        }
        """
        if '$commit' not in kwargs:
            raise db.DataBaseConditionError('missing commit')
        commit = kwargs.pop('$commit')
        result = self.__connexion.update(self._model.__name__, **kwargs, **commit)
        if not result:
            raise db.DataBaseUpdateError('update failed')
        if isinstance(result, dict):
            return Scalar(self.__model(**result), self)
        else:
            return Matrix(*[self._model(**item) for item in result]) if result else None

    def delete(self, **kwargs) -> None:
        """
        kwargs: {
            'field': 'value',
            'field': 'value',
            ...
        }
        """
        self.__connexion.delete(self._model.__name__, **kwargs)
