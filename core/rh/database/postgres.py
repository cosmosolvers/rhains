""""""
from .adapter import Adapter, Rowscrud, Tablecrud, Datacrud
import psycopg2


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
        except:
            pass


class PostgresCRUD(Rowscrud):
    pass


class PostgresTablecrud(Tablecrud):
    pass


class PostgresDatacrud(Datacrud):
    pass




# -- Correspondance partielle
# SELECT * FROM users WHERE name ~ 'A.*';

# -- Correspondance totale
# SELECT * FROM users WHERE name ~ '^A.*$';