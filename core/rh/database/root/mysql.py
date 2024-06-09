""""""
from ..adapter import Adapter, Rowscrud, Tablecrud, Datacrud
import MySQLdb


class MysqlAdapter(Adapter):
    def connect(self):
        try:
            self._client: MySQLdb.connections.Connection = MySQLdb.connect(
                host=self.conf.get('host'),
                user=self.conf.get('user'),
                password=self.conf.get('pwd'),
                database=self.conf.get('name'),
                port=int(self.conf.get('port'))
            )
        except:
            pass


class MysqlCRUD(Rowscrud):
    pass


class MysqlDatacrud(Datacrud):
    pass


class MysqlTablecrud(Tablecrud):
    pass


# -- Correspondance partielle
# SELECT * FROM users WHERE name REGEXP 'A.*';

# -- Correspondance totale
# SELECT * FROM users WHERE name REGEXP '^A.*$';