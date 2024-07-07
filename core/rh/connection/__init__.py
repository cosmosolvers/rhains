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

CREATE
======

{
    '$push': {
        'field': 'value',
        'field': 'value',
        ...
    }
}


GET
===


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
            {'$.': '!'},
        ]
    }
}

UPDATE
======

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

DELETE
======

{
    '$del': {
        'field': 'value',
        'field': 'value',
        ...
    }
}

the agents
----------
s'appliquent uniquement sur un pull

1. all
    {'$.': '*'}
2. exists v
    {'$.': '!'}
3. count v
    {'$.': '?'}
4. sort v
    {'$sort': 'field'}
5. limit v
    {'$.': (0, n)}
6. exclude v
    {'$-': {'field': 'value'}}
8. first v
    {'$.': 0}
9. last v
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
13. partial
    {'$rm': value} / {'$add': value}
    item
    {'$!': value} elt de elt


the keys
--------
1. many
    {'$': [] }

2. atomic
    {'$atomic': True} default False


the meta
--------
1. aggregation
    {'$agg': {'field': 'value'}}

"""
from ..database import (
    SqliteCRUD,
    PostgresCRUD,
    MysqlCRUD,
    MongoDBCRUD,
    ArangoDBCRUD
)
from .collection import Collection


instruct = {
    'sqlite': SqliteCRUD,
    'mysql': MysqlCRUD,
    'postgres': PostgresCRUD,
    'mongodb': MongoDBCRUD,
    'Arangodb': ArangoDBCRUD
}


class Connection:
    def __init__(self, **kwargs) -> None:
        self.__connexion = instruct.get(kwargs.get('engine'))(kwargs.get('session'))
        self.__model = kwargs.get('model')
        self.tablename = str(self.__model.__name__).lower()

    def __get__(self, instance, owner) -> Collection | None:
        if instance is None:
            return self
        return Collection(self.__model, self.__connexion) if self.__model else None

    # @property
    # def collection(self) -> Collection:
    #     return Collection(self.__model, self.__connexion)


__all__ = ['Connection']
