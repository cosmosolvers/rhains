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
# import re

from utils.data import pk

from exceptions.core.rh import database as db


# def regexp(pattern, string):
#     if string is None:
#         return None
#     return re.search(pattern, string) is not None


class SqliteAdapter(Adapter):
    def connect(self):
        try:
            self._client: sqlite3.Connection = sqlite3.connect(
                self._conf.get('name'),
                detect_types=sqlite3.PARSE_DECLTYPES,
            )
            self._client.row_factory = sqlite3.Row
            self._client.execute('PRAGMA foreign_keys = ON')
            # self._client.create_function('REGEXP', 2, regexp)
        except sqlite3.Error as e:
            raise db.DatabaseError(e)


class SqliteCRUD(Rowscrud):
    def __init__(self, connexion: sqlite3.Connection) -> None:
        self.connexion = connexion

    def bulk_create(self, conn, tablename: str, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        # retourner les valeur des pk pour les foreignkeys
        pk(kwargs.values())
        values = tuple(kwargs.values())
        query = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid

    def bulk__update(self, conn, tablename: str, **kwargs):
        primarykey = kwargs.get('$pk')
        commit = kwargs.get('$commit')

        placeholders = ' AND '.join([f'{key} = ?' for key in primarykey])
        updating = ' ,'.join(f"{key} = ?" for key in commit)
        values = tuple(commit.values()) + tuple(primarykey.values())

        query = f"UPDATE {tablename} SET {updating} WHERE {placeholders}"
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid

    def bulk_get(self, conn, tablename: str, **kwargs):
        column, value = kwargs.popitem()
        query = f"SELECT * FROM {tablename} WHERE {column} = ?"
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(query, (value, ))
        result = cursor.fetchone()
        return result

    def bulk_all(self, conn, tablename: str):
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {tablename}')
        result = cursor.fetchall()
        return result

    def bulk_filter(self, conn, tablename: str, *args, **kwargs):
        placeholders = ' AND '.join([f'{key} = ?' for key in kwargs])
        values = tuple(kwargs.values())
        query = f"SELECT * FROM {tablename} WHERE {placeholders}"
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        return result

    def create(self, tablename: str, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        # retourner les valeur des pk pour les foreignkeys
        pk(kwargs.values())
        values = tuple(kwargs.values())
        query = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"

        with session(self.connexion) as conn:
            try:
                cursor: sqlite3.Cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                raise db.DatabaseError(str(e))

    def get(self, tablename: str, **kwargs):
        column, value = kwargs.popitem()
        query = f"SELECT * FROM {tablename} WHERE {column} = ?"

        with session(self.connexion) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(query, (value, ))
            result = cursor.fetchone()
            return result

    def all(self, tablename: str):
        with session(self.connexion) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {tablename}')
            result = cursor.fetchall()
            return result

    def filter(self, tablename: str, *args, **kwargs):
        placeholders = ' AND '.join([f'{key} = ?' for key in kwargs])
        values = tuple(kwargs.values())
        query = f"SELECT * FROM {tablename} WHERE {placeholders}"

        with session(self.connexion) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(query, values)
            result = cursor.fetchall()
            return result

    def update(self, tablename: str, **kwargs):
        primarykey = kwargs.get('$pk')
        commit = kwargs.get('$commit')

        placeholders = ' AND '.join([f'{key} = ?' for key in primarykey])
        updating = ' ,'.join(f"{key} = ?" for key in commit)
        values = tuple(commit.values()) + tuple(primarykey.values())

        query = f"UPDATE {tablename} SET {updating} WHERE {placeholders}"

        with session(self.connexion) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid

    def delete(self, tablename: str, **kwargs):
        key, value = kwargs.get('$pk').popitem()
        query = f"DELETE FROM {tablename} WHERE {key} = ?"

        with session(self.connexion) as conn:
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute(query, (value, ))
            conn.commit()
            return cursor.rowcount > 0


class SqliteTablecrud(Tablecrud):
    pass


class SqliteDatacrud(Datacrud):
    pass
