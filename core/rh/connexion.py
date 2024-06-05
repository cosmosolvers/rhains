"""
primary syntax
==============
create : '$push'
list   : '$pull'
get    : '$get'
update : '$set'
delete : '$del'

create syntax
=============
{
    '$push': {
        'field': 'value',
        'field': 'value',
        ...
    }
}

get syntax
==========
1. simple get
{
    '$get': {
        '$pk': {'field': 'value'}
    }
}
2. get with primary condition
{
    '$get': {
        '$pk': {'field': 'value'},
        'field': 'value',
        'field1': {'$lt': 'value'}
    }
}
3. get with foreign key
{
    '$get': {
        '$pk': {'field': 'value'},
        'field': 'value',
        # lorsque vous voulez mettre une condition sur un/plusieurs
        # champ de la table associer a la fk
        'field1': {'$fk': {
            'field': 'value',
            ...
            }
        }
    }
}

list syntax
===========
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
        '$pk': {'field': 'value'},
        'field': {'$fk': {'field': 'value}}
    }
}
4. utiliser les agents
{
    '$pull': {
        'field': 'value',
        'field': {'$gt': 'value'}
        '$': {
            {'$-': {'field': 'value'}},
            {'$.': '!'}
        }
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
=============
{
    '$set': {
        '$pk': {'field': 'value'},
        ...
    }
}

delete syntax
=============
{
    '$del': {
        '$pk': {'field': 'value'},
        ...
    }
}

the agents
==========
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

the requirements
================
s'appliquent uniquement sur les functions $get, $del, $set

1. pk
    {'$pk': {'field': 'value'}}
2. fk
    {'$fk': {'field': 'value'}}

the conditions
===============
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
    {'$ge': value}
6. not in
    {'$in': value}
7. not equal
    {'$ne': value}
8. like
    {'$like': value}
10. min
    {'$min': value}
11. max
    {'$max': value}
12. avg
    {'$avg': value}
4. partial, complete, remove
    {'$rm': value} / {'$add': value} / {'$set': value}

the keys
========
1. many
    {'$': }

the meta
========
1. aggregation
    {'$agg': {'field': 'value'}}
"""
from typing import Dict

from exception.core.rh import database as data

from .result import (
    RhesultOne,
    RhesultDictOne,
    RhesultMany,
    RhesultDictMany,
    RhesultNone,
    RhesultDictNone
)
from .database import (
    SqliteAdapter,
    SqliteCRUD,

    PostgresAdapter,
    PostgresCRUD,

    MysqlAdapter,
    MysqlCRUD,

    MongoDBAdapter,
    MongoDBCRUD,

    ArangoDBAdapter,
    ArangoDBCRUD
)
from .session import session_manager

adaptor = {
    'sqlite': SqliteAdapter,
    'mysql': MysqlAdapter,
    'postgres': PostgresAdapter,
    'mongodb': MongoDBAdapter,
    'Arangodb': ArangoDBAdapter
}

instruct = {
    'sqlite': SqliteCRUD,
    'mysql': MysqlCRUD,
    'postgres': PostgresCRUD,
    'mongodb': MongoDBCRUD,
    'Arangodb': ArangoDBCRUD
}


class Collection:
    def __init__(self, model) -> None:
        self._model = model
        self.res = self._model.Meta.result
        engine, connexion = session_manager.get_connexion(
            self._model.Meta.database
        )
        self._instruct = instruct.get(engine)(connexion)

    def collect(self, **kwargs):
        if kwargs:
            if len(kwargs) != 1:
                raise data.DataBaseConditionError('too many arguments')
            key, value = kwargs.popitem()
            if key == '$push':
                return self._create(**value)
            if key == '$get':
                return self._get(**value)
            if key == '$pull':
                if len(value) == 1 and '$' in value:
                    return self._all()
                return self._filter(**value)
            if key == '$set':
                return self._update(**value)
            if key == '$del':
                return self._delete(**value)
            if key == '$':
                return self.collect(**value)
        return self._all()

    def _create(self, **kwargs) -> RhesultOne | RhesultDictOne:
        """_summary_
        Returns:
            RhesultOne | RhesultDictOne: _description_
        """
        # cree un objet du model
        entry = self._model(**kwargs)
        # recupere l'objet sous forme de dictionnaire
        entry = self._to_dict(entry)
        # cree l'objet dans la base de donnee
        result = self._instruct.create(self._model.__name__, **entry)
        return RhesultOne(self, dict(result))\
            if self.res == 'dict' else RhesultDictOne(self, dict(result))

    def _get(self, **kwargs) -> RhesultOne | RhesultDictOne | None:
        if '$pk' in kwargs:
            # seul un pull est autoriser a avoir '$' comme argument direct
            if '$' in kwargs:
                raise data.DataBaseConditionError('$get not allowed with $')
            pk = kwargs.pop('$pk')
            pk_column, pk = pk.popitem()
            kwargs = self._recap_data(pk_column, kwargs)
            result = self._instruct.get(self._model.__name__, pk, pk_column, **kwargs)
            return RhesultOne(self, dict(result))\
                if self.res == 'dict' else RhesultDictOne(self, dict(result))
        else:
            raise data.DataBaseConditionError('missing primary key')

    def _all(self) -> RhesultMany | RhesultDictMany:
        result = self._instruct.all(self._model.__name__)
        result = [
            RhesultOne(self, dict(item)) if self.res == 'dict' else RhesultDictOne(self, dict(item))
            for item in result
        ]
        return RhesultMany(self, result)\
            if self.res == 'dict' else RhesultDictMany(self, result)

    def _filter(self, **kwargs) -> RhesultMany | RhesultDictMany:
        for key, value in kwargs.items():
            if '$fk'
        result = self._instruct.filter(self._model.__name__, **kwargs)
        result = [
            RhesultOne(self, dict(item)) if self.res == 'dict' else RhesultDictOne(self, dict(item))
            for item in result
        ]
        return RhesultMany(self, result)\
            if self.res == 'dict' else RhesultDictMany(self, result)

    def _update(self, pk, **kwargs) -> RhesultOne | RhesultDictOne | None:
        result = self._instruct.update(self._model.__name__, pk, **kwargs)
        return RhesultOne(self, dict(result))\
            if self.res == 'dict' else RhesultDictOne(self, dict(result))

    def _delete(self, **kwargs) -> RhesultNone | RhesultDictNone | None:
        self._instruct.delete(self._model.__name__, **kwargs)
        return RhesultNone(self)\
            if self.res == 'dict' else RhesultDictNone(self)

    def _to_dict(self, obj):
        return {
            key: getattr(obj, key)
            for key in obj.__dict__
            if not key.startswith('_') and not callable(getattr(obj, key))
        }

    def _recap_data(self, key, data: Dict):
        if '$fk' in data[:]:
            data['$fk']['model'] = getattr(self._model, key).meta.foreignkey
            for key, value in data['$fk'].items():
                if key == 'model':
                    continue
                self._recap_data(key, value)
        return data


# databases configuration (manage)
# a charger depuis un fichier de configuration
# avant de lancer le serveur
# Model._service = (au service charger)
class Service:
    def __init__(self, conf: Dict, *args, **kwargs) -> None:
        for key, data in conf.items():
            session_manager.register(
                key,
                data.get('engine'),
                adaptor.get(data.get('engine'))(data)
            )


class Connexion:
    """
    Connexion
    =========
    """

    def __init__(self, tablemodel, *args, **kwargs) -> None:
        # table model
        self._tablemodel = tablemodel
        engine, connexion = session_manager.get_connexion(
            self._tablemodel.Meta.database
        )
        self._instruct = instruct.get(engine)(connexion)

    def create(self, **kwargs) -> RhesultOne:
        result = self._instruct.create(self._tablemodel.__name__, **kwargs)
        return RhesultOne(self, dict(result))

    def get(self, pk, **kwargs) -> RhesultOne | None:
        result = self._instruct.get(self._tablemodel.__name__, pk, **kwargs)
        return RhesultOne(self, dict(result)) if result else None

    def get_or_create(self, pk, **kwargs) -> RhesultOne:
        result = self.get(pk, **kwargs)
        if not result:
            result = self.create(**kwargs)
        return result

    def all(self) -> RhesultMany:
        result = self._instruct.all(self._tablemodel.__name__)
        result = [RhesultOne(self, dict(item)) for item in result]
        return RhesultMany(self, result)

    def filter(self, **kwargs) -> RhesultMany:
        result = self._instruct.filter(self._tablemodel.__name__, **kwargs)
        result = [RhesultOne(self, dict(item)) for item in result]
        return RhesultMany(self, result, **kwargs)

    def update(self, pk, **kwargs) -> RhesultOne | None:
        result = self._instruct.update(self._tablemodel.__name__, pk, **kwargs)
        return RhesultOne(self, dict(result)) if result else None

    def get_or_update(self, pk, **kwargs) -> RhesultOne | None:
        result = self.get(pk, **kwargs)
        if not result:
            result = self.update(pk, **kwargs)
        return result

    def delete(self, **kwargs) -> RhesultNone | None:
        self._instruct.delete(self._tablemodel.__name__, **kwargs)
        return RhesultNone(self)

    def aggregate(self, **kwargs) -> RhesultMany:
        result = self._instruct.aggregate(
            self._tablemodel.__name__, **kwargs
        )
        result = [RhesultOne(self, dict(item)) for item in result]
        return RhesultMany(self, result, **kwargs)

    def collect(self, action: Dict):
        pass

    @property
    def instruct(self):
        return self._instruct, self._tablemodel.__name__
