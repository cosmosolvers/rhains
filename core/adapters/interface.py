""""""

from typing import List


class SQLAdapterInterface:
    
    def connect(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")
    
    def execute(self, query: str, values=None, fetch: bool=False, commit: bool=False, *args, **kwargs):
        raise NotImplementedError("Method not implemented")
    
    def close(self):
        raise NotImplementedError("Method not implemented")



class NOSQLAdapterInterface:
    
    pass
