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
from utils.data import pk

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
            raise db.DatabaseError(e)


class SqliteCRUD(Rowscrud):
    def __init__(self, connexion: sqlite3.Connection) -> None:
        self.connexion = connexion

    def atomic(self, **kwrags):
        with session(self.connexion) as conn:
            try:
                pass
            except sqlite3.Error as e:
                conn.rollback()
                raise db.DatabaseError(str(e))

    def create(self, tablename: str, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        # retourner les valeur des pk pour les foreignkeys
        pk(kwargs.values())
        values = tuple(kwargs.values())
        query = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"

        with session(self.connexion) as connexion:
            try:
                cursor: sqlite3.Cursor = connexion.cursor()
                cursor.execute(query, values)
                connexion.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                raise db.DatabaseError(str(e))

    def get(self, tablename: str, **kwargs):
        values = kwargs.popitem()
        query = f"SELECT * FROM {tablename} WHERE ? = ?"

        with session(self.connexion) as connexion:
            cursor: sqlite3.Cursor = connexion.cursor()
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result

    def all(self, tablename: str):
        with session(self.connexion) as connexion:
            cursor: sqlite3.Cursor = connexion.cursor()
            cursor.execute(f'SELECT * FROM {tablename}')
            result = cursor.fetchall()
            return result

    def filter(self, tablename: str, *args, **kwargs):
        placeholders = ', '.join(['? = ?' for _ in kwargs])
        values = tuple(kwargs.values())
        query = f"SELECT * FROM {tablename} WHERE {placeholders}"

        with session(self.connexion) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(query, values)
            result = cursor.fetchall()
            return result

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
