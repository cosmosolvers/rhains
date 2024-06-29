""""""
# from .interface import SqlInterface
from ..adapter import (
    Adapter,
    Rowscrud,
    Tablecrud,
    Datacrud
)

from ...session import session

import sqlite3
import re

from utils.condition import CONDITION
from exceptions.core.rh import database as db


def regexp(pattern, string):
    if string is None:
        return None
    return re.search(pattern, string) is not None


class SqliteAdapter(Adapter):
    def connect(self):
        try:
            self._client: sqlite3.Connection = sqlite3.connect(
                self._conf.get('name'),
                detect_types=sqlite3.PARSE_DECLTYPES,
            )
            self._client.row_factory = sqlite3.Row
            self._client.execute('PRAGMA foreign_keys = ON')
            self._client.create_function('REGEXP', 2, regexp)
        except sqlite3.Error as e:
            raise db.DatabaseError(str(e))


class SqliteCRUD(Rowscrud):
    def __init__(self, connexion: sqlite3.Connection) -> None:
        self.connexion = connexion
        # creer une memoire cache temporaire pour les conditions having
        # a executer apres le rendu de la base de donnée
        # elle doit etre vider avant chaque requete
        self.__ATOMIC = False

    def create(self, tablename: str, **kwargs):
        self.__ATOMIC = kwargs.pop('$atomic', False)
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = tuple(kwargs.values())
        query = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"

        with session(self.connexion) as connexion:
            try:
                cursor: sqlite3.Cursor = connexion.cursor()
                cursor.execute(query, values)
                connexion.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                if self.__ATOMIC:
                    connexion.rollback()
                raise db.DatabaseError(str(e))

    def get(self, tablename: str, **kwargs):
        self.memory.clear()
        join, where, having, values = self._query(tablename, '$get', **kwargs)
        query = f"""
        SELECT * FROM {tablename}
        """ + join + where + having

        with session(self.connexion) as connexion:
            cursor: sqlite3.Cursor = connexion.cursor()
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result

    def _query(self, tab, func: str, **kwargs):
        join = ''
        where = 'pk = ?' if func in ('$get', '$set', '$del') else ''
        having = ''
        values = (kwargs.get('$pk'),) if func in ('$get', '$set') else tuple()
        for key, data in kwargs.items():
            if '$fk' in data:
                # recuperer la table de la clé etrangere
                tab1 = data['$fk'].get('model')
                # faire un join
                join += f' JOIN {tab1} ON {tab}.{key} = {tab1}.pk'
                # recommencer le processus avec le reste des elements de la table etrangere
                j, w, h, v = self._query(tab1, func, data['$fk'])
                # collecter les resultats
                join += f' {j}'
                where += f"{' AND ' if where else ''}{w}"
                having += f"{' AND ' if where else ''}{h}"
                values += v
            if not isinstance(data, dict):
                where += f'{' AND' if where else ''}{tab}.{key} = {data}'
            if isinstance(data, dict):
                k, s = data.popitem()
                if k in CONDITION:
                    w, v = CONDITION.get(k)(tab, k, s)
                    where += w
                    values += v
                else:
                    self.memory[key] = k

    def _join_query(self, tab, key, data):
        new_tab = data.get('model')
        join = f' JOIN {new_tab} ON {tab}.{key} = {new_tab}.pk'
        return join

    def _agent_query(self, tab, key, data):
        pass

    def _where_query(self, tab, key, data):
        pass

    def _memory_query(self, tab, key, data):
        pass

    def all(self, tablename: str):
        with session(self.connexion) as connexion:
            cursor: sqlite3.Cursor = connexion.cursor()
            cursor.execute(f'SELECT * FROM {tablename}')
            result = cursor.fetchall()
            return result

    def filter(self, tablename: str, *args, **kwargs):
        query = f"""
        SELECT * FROM {tablename}
        """

    # faire un get avant l'operation dans les update
    # pour la possibilité de manipuler les list, dict et tuple enregistrer en json
    def update(self, tablename: str, **kwargs):
        self.memory.clear()
        join, where, having, values = self._query(tablename, '$set', **kwargs)
        query = f"""
        SELECT * FROM {tablename}
        """

    def delete(self, tablename: str, pk, *args, **kwargs):
        where = ''
        having = ''
        join = ''
        values = tuple()
        query = f"""
        SELECT * FROM {tablename}
        """

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


class SqliteTablecrud(Tablecrud):
    pass


class SqliteDatacrud(Datacrud):
    pass
