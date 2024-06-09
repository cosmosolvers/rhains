""""""
from ..adapter import Adapter, Rowscrud, Tablecrud, Datacrud
import pymongo


class MongoDBAdapter(Adapter):
    def connect(self):
        try:
            self._client = pymongo.MongoClient(
                host=self.conf.get('host'),
                port=self.conf.get('port'),
                username=self.conf.get('user'),
                password=self.conf.get('pwd')
            )
        except:
            pass


class MongoDBCRUD(Rowscrud):
    pass


class MongoDBDatacrud(Datacrud):
    pass


class MongoDBTablecrud(Tablecrud):
    pass
