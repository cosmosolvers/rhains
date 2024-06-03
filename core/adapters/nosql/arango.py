""""""
from core.adapters import interface
from arango import ArangoClient




class ArangoAdapter(interface.Interface):
    
    def connect(self, *args, **kwargs):
        """
        hosts
        """
        self.cursor = ArangoClient(*args, **kwargs)
        sysdb = self.cursor.db('_system', username=kwargs.get('username', 'root'), password=kwargs.get('passwd', 'password'))
        
        if not sysdb.has_collection(kwargs.get('dbname')):
            sysdb.create_database(kwargs.get('dbname'))
            
        self.database = self.cursor.db(kwargs.get('dbname'))
    
    def close(self):
        self.cursor.close()
