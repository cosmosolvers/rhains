""""""
import arango.database
from .adapter import Adapter, Rowscrud, Tablecrud, Datacrud
import arango
from typing import Dict


class ArangoDBAdapter(Adapter):
    def connect(self):
        try:
            self._client = arango.ArangoClient(
                host=self.conf.get('host'),
                port=self.conf.get('port'),
                username=self.conf.get('user'),
                password=self.conf.get('pwd')
            )
        except:
            pass


class ArangoDBCRUD(Rowscrud):
    pass


class ArangoDBTablecrud(Tablecrud):
    pass


class ArangoDBDatacrud(Datacrud):
    pass
