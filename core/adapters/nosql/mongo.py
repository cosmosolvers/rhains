""""""
from core.adapters import interface
import pymongo



class MongoAdapter(interface.Interface):
    
    def connect(self, *args, **kwargs):
        """
        username
        password
        host
        port: 27017
        db
        """
        self.cursor = pymongo.MongoClient(*args, **kwargs)
        self.database = self.cursor[kwargs.get('dbname')]
    
    def close(self):
        self.cursor.close()