""""""
# from .interface import SqlInterface
from .adapter import (
    Adapter,
    Rowscrud,
    Tablecrud,
    Datacrud
)
from ..session import session
import sqlite3
import re

from exception.core.rh import database as data


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
            raise data.DatabaseError(str(e))


class SqliteCRUD(Rowscrud):
    def __init__(self, connexion: sqlite3.Connection) -> None:
        self.connexion = connexion

    def create(self, tablename: str, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = tuple(kwargs.values())
        query = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"

        with session(self.connexion) as connexion:
            cursor: sqlite3.Cursor = connexion.cursor()
            cursor.execute(query, values)
            connexion.commit()
            return cursor.lastrowid

    def get(self, tablename: str, pk, primary_key='id', **kwargs):
        join, where, having, values = self._ready_query(tablename, **kwargs)
        query = f"""
        SELECT * FROM {tablename}
        """ + join + where + f' WHERE {primary_key} = ?;'
        values += (pk,)

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
        where = ''
        having = ''
        join = ''
        values = tuple()
        query = f"""
        SELECT * FROM {tablename}
        """

    def update(self, tablename: str, pk, *args, **kwargs):
        where = ''
        having = ''
        join = ''
        values = tuple()
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
