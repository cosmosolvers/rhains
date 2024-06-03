""""""

from adapters import interface

from typing import Dict





class Rows:...




class DataTable:
    """"""
    
    def __init__(self, database, tablename: str) -> None:
        
        self.database = database
        self.collection = self.database[tablename]
        self.rows = Rows(self.collection)
    
    def create(self, columns: Dict):
        pass