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
        '$pk': 'value'
    }
}
2. get with primary condition
{
    '$get': {
        '$pk': 'value',
        'field': 'value',
        'field1': {'$lt': 'value'}
    }
}
3. get with foreign key
{
    '$get': {
        '$pk': 'value',
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
        '$pk': 'value',
        'field': {'$fk': {'field': 'value}}
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
=============
{
    '$set': {
        '$pk': 'value',
        ...,
        '$update': {
            'field': value,
            # les champs de list, tuple, dict
            'field': {'$rm': value},
            'field': {'$add': value},
        }
    }
}

delete syntax
=============
{
    '$del': {
        '$pk': 'value',
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
    $pk': 'value'
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
========
1. many
    {'$': }

the meta
========
1. aggregation
    {'$agg': {'field': 'value'}}
"""
from typing import Dict

from exception.core.rh.database import collection as db

from .result import (
    Success,
    Fails,

    StoredKey,
    StoredKeyList,

    Vector,
    VectorList
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
                raise db.DataBaseConditionError('too many arguments')
            key, value = kwargs.popitem()
            match key:
                case '$get': return self._get(value)
                case '$set': return self._update(value)
                case '$del': return self._delete(value)
                case '$push': return self._create(value)
                case '$pull': return self._filter(value)
                case '$':
                    if not isinstance(value, list):
                        raise db.DataBaseFieldTypeError(f"{value} must be list")
                    args = []
                    for val in value:
                        args.append(self.collect(**val))
                    return tuple(args)
        return self._all()

    def _create(self, data):
        if not isinstance(data, dict):
            raise db.DataBaseFieldTypeError(f"{data} must be dict")
        return self._bulk_create(**data)

    def _bulk_create(self, **kwargs) -> StoredKey | Vector:
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
        return Vector(self, dict(result))\
            if self.res == 'dict' else StoredKey(self, dict(result))

    def _get(self, data):
        if not isinstance(data, dict):
            raise db.DataBaseFieldTypeError(f"{data} must be dict")
        return self._bulk_get(**data)

    def _bulk_get(self, **kwargs) -> StoredKey | Vector | None:
        if '$pk' in kwargs:
            # seul un pull est autoriser a avoir '$' comme argument direct
            if '$' in kwargs:
                raise db.DataBaseConditionError('$get not allowed with $')
            self._recap_data(kwargs)
            result = self._instruct.get(self._model.__name__, **kwargs)
            return Vector(self, dict(result))\
                if self.res == 'dict' else StoredKey(self, dict(result))
        else:
            raise db.DataBaseConditionError('missing primary key')

    def _all(self) -> VectorList | StoredKeyList:
        result = self._instruct.all(self._model.__name__)
        result = [
            Vector(self, dict(item)) if self.res == 'dict' else StoredKey(self, dict(item))
            for item in result
        ]
        return VectorList(self, result)\
            if self.res == 'dict' else StoredKeyList(self, result)

    def _filter(self, data):
        if not isinstance(data, dict):
            raise db.DataBaseFieldTypeError(f"{data} must be dict")
        if len(data) == 1 and '$' in data:
            return self._all()
        return self._bulk_filter(**data)

    def _bulk_filter(self, **kwargs) -> VectorList | StoredKeyList:
        self._recap_data(kwargs)
        result = self._instruct.filter(self._model.__name__, **kwargs)
        result = [
            Vector(self, dict(item)) if self.res == 'dict' else StoredKey(self, dict(item))
            for item in result
        ]
        return VectorList(self, result)\
            if self.res == 'dict' else StoredKeyList(self, result)

    def _update(self, data):
        if not isinstance(data, dict):
            raise db.DataBaseFieldTypeError(f"{data} must be dict")
        return self._update(**data)

    def _bulk_update(self, **kwargs) -> StoredKey | Vector | None:
        if '$pk' in kwargs:
            # seul un pull est autoriser a avoir '$' comme argument direct
            if '$' in kwargs:
                raise db.DataBaseConditionError('$get not allowed with $')
            self._recap_data(kwargs)
        result = self._instruct.update(self._model.__name__, **kwargs)
        return Vector(self, dict(result))\
            if self.res == 'dict' else StoredKey(self, dict(result))

    def _delete(self, data):
        if not isinstance(data, dict):
            raise db.DataBaseFieldTypeError(f"{data} must be dict")
        return self._delete(**data)

    def _bulk_delete(self, **kwargs) -> Success | Fails :
        if '$pk' in kwargs:
            # seul un pull est autoriser a avoir '$' comme argument direct
            if '$' in kwargs:
                raise db.DataBaseConditionError('$get not allowed with $')
            self._recap_data(kwargs)
        result = self._instruct.delete(self._model.__name__, **kwargs)
        return Success if result else Fails

    def _to_dict(self, obj):
        return {
            key: getattr(obj, key)
            for key in obj.__dict__
            if not key.startswith('_') and not callable(getattr(obj, key))
        }

    def _recap_data(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                if '$fk' in value.keys():
                    value['$fk']['model'] = getattr(self._model, key).meta.foreignkey.__name__
                    self._recap_data(value)

    @property
    def instruct(self):
        return self._instruct


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
