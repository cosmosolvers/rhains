""""""
from typing import Dict, List
import json

from exception.core.rh import database as db


def ready_query(self, tablename: str, **kwargs):
    where = ''
    values = tuple()
    having = []
    join = ''

    def handle_operator(key, operator, value):
        nonlocal where, values
        if operator in ('min', 'max', 'sum', 'avg'):
            having.append((key, operator, value))
        else:
            cond = handle_where(where, value, operator, key)
            where += cond[0]
            values += cond[1]

    def handle_key_value(key, value):
        nonlocal where, values
        where += f'{" AND" if where else ""}{key} = ?'
        values += (value,)

    if kwargs and len(kwargs) > 0:
        for key, value in kwargs.items():
            if '::' in key:
                key, *operator = key.split('::')
                if len(operator) == 0:
                    raise db.DataFieldError(f"{key} is badly built")
                if len(operator) == 1:
                    operator = operator[0]
                    handle_operator(key, operator, value)
                else:
                    # operator est une liste de fk les uns après les autres
                    # operator[-1] est soit le champ de la table de la derniere fk
                    # soit un des opérateurs de comparaison
                    before = tablename
                    for i in operator[:-1]:
                        join += f'INNER JOIN {i} ON {before}.{i} = {i}.{pk} '
                        before = i
                    operator = operator[-1]
                    handle_operator(key, operator, value)
            else:
                handle_key_value(key, value)

    return join, where, having, values


def handle_where(self, where: str, value, operator: str, key: str):
    if operator == 'reg':
        return f"{' AND' if where else ''} {key} REGEXP ?", (value,)
    elif operator == 'ireg':
        return f"{' AND' if where else ''} {key} REGEXP '(?i)' || ?", (value,)
    elif operator == 'in':
        return f'{" AND" if where else ""}{key} IN (?)', (value,)
    elif operator == 'lt':
        return f'{" AND" if where else ""}{key} < ?', (value,)
    elif operator == 'gt':
        return f'{" AND" if where else ""}{key} > ?', (value,)
    elif operator == 'ne':
        return f'{" AND" if where else ""}{key} != ?', (value,)
    elif operator == 'le':
        return f'{" AND" if where else ""}{key} <= ?', (value,)
    elif operator == 'ge':
        return f'{" AND" if where else ""}{key} >= ?', (value,)
    elif operator == 'nin':
        return f'{" AND" if where else ""}{key} NOT IN (?)', (value,)
    elif operator == 'bet':
        return f'{" AND" if where else ""}{key} BETWEEN ? AND ?', value
    elif operator not in connector:
        # key est une fk et operator un champ de la table de la fk
        return f'{" AND" if where else ""}{key}.{operator} = ?', (value,)


def handle_having(self, having: list, result: List[Dict]):
    for key, operator, value in having:
        value = json.loads(value)
        if operator == 'min':

            result[key] = min(result[key])
        elif operator == 'max':
            result[key] = max(result[key])
        elif operator == 'sum':
            result[key] = sum(result[key])
        elif operator == 'avg':
            result[key] = sum(result[key]) / len(result[key])
    return result


def avg(*args):
    return sum(args) / len(args)


def iterable(result: List[Dict], key, value, operator):
    func = {
        'min': min,
        'max': max,
        'sum': sum,
        'avg': avg
    }

    for res in result[:]:
        
        if min(json.loads(res[key])) > value:
            result.remove(res)
    return result


class Adapter:

    def __init__(self, conf: Dict) -> None:
        self._conf = conf
        self._client = None

    def connect(self):
        """database create en connect"""
        raise NotImplementedError("Method not implemented")

    @property
    def connexion(self):
        return self._client

    def close(self):
        """databse close"""
        if self._client:
            self._client.close()


class Rowscrud:
    def __init__(self, connexion) -> None:
        pass

    def create(self, *args, **kwargs):
        pass

    def get(self, pk, *args, **kwargs):
        pass

    def all(self):
        pass

    def filter(self, *args, **kwargs):
        pass

    def update(self, pk, *args, **kwargs):
        pass

    def delete(self, pk, *args, **kwargs):
        pass

    def aggregations(self, *args, **kwargs):
        pass

    def exists(self, *args, **kwargs):
        pass

    def count(self, *args, **kwargs):
        pass

    def sort(self, *args, **kwargs):
        pass

    def limit(self, *args, **kwargs):
        pass

    def offset(self, *args, **kwargs):
        pass


class Tablecrud:
    def __init__(self, connexion) -> None:
        pass

    # create table
    def create(self, *args, **kwargs):
        pass

    # list all tables to database
    def list(self, *args, **kwargs):
        pass

    # delete table
    def delete(self, *args, **kwargs):
        pass

    # alter table
    def update(self, *args, **kwargs):
        pass

    # number of tables to database
    def count(self):
        pass


class Datacrud:
    def __init__(self, connexion) -> None:
        pass

    def create(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def backup(self, *args, **kwargs):
        pass


class DataTableAdapter:

    def __init__(self, *args, **kwargs) -> None:
        pass

    def read(self, *args, **kwargs):
        """select"""
        pass

    def one(self, pk, *args, **kwargs):
        """select one"""
        pass

    def all(self):
        """select all"""
        pass

    def write(self, *args, **kwargs):
        """insert"""
        pass

    def update(self, pk, *args, **kwargs):
        """update"""
        pass

    def remove(self, pk=None, *args, **kwargs):
        """delete"""
        pass

    def limit(self, *args, **kwargs):
        pass

    def count(self):
        """count"""
        pass

    def exists(self):
        """exists"""
        pass

    def drop(self, *args, **kwargs):
        pass

    def alter(self, *args, **kwargs):
        pass

    def aggregations(self, *args, **kwargs):
        pass


class Manager:

    def __init__(self, *args, **kwargs) -> None:
        pass

    def backup(self, *args, **kwargs):
        pass

    def restore(self, *args, **kwargs):
        pass

    # drop database
    def drop(self, *args, **kwargs):
        pass

    # list all tables in database
    def tables(self, *args, **kwargs):
        pass

    # table number
    def count(self):
        pass

    # create database
    def create(self, *args, **kwargs):
        pass


__all__ = ['Adapter', 'DataTableAdapter', 'Manager']
