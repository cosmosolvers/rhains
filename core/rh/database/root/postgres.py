""""""
from ..adapter import Adapter, Rowscrud, Tablecrud, Datacrud
import psycopg2

from exceptions.core.rh import database as db


class PostgresAdapter(Adapter):
    def connect(self):
        try:
            self._client = psycopg2.connect(
                dbname=self.conf.get('name'),
                user=self.conf.get('user'),
                password=self.conf.get('pwd'),
                host=self.conf.get('host'),
                port=self.conf.get('port')
            )
        except psycopg2.DatabaseError as e:
            raise db.DatabaseError(e)


class PostgresCRUD(Rowscrud):
    def __init__(self, connexion: psycopg2.extensions.connection) -> None:
        self.connexion = connexion
        self.__ATOMIC = False


class PostgresTablecrud(Tablecrud):
    pass


class PostgresDatacrud(Datacrud):
    pass


# -- Correspondance partielle
# SELECT * FROM users WHERE name ~ 'A.*';

# -- Correspondance totale
# SELECT * FROM users WHERE name ~ '^A.*$';
