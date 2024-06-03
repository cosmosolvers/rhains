""""""

from typing import List




class Interface:
    
    def connect(self, *args, **kwargs):
        pass

    def close(self):
        pass



class SQLAdapterInterface(Interface):
    
    def connect(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")
    
    def execute(self, query: str, values=None, fetch: bool=False, commit: bool=False, *args, **kwargs):
        raise NotImplementedError("Method not implemented")
    
    def close(self):
        raise NotImplementedError("Method not implemented")


