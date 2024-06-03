from .adapter import DataTable
from .sqlite import SQLiteAdapter
from .mysql import MySQLAdapter
from .postgres import PostgreSQLAdapter

from core.adapters import interface



adapter = {
    "sqlite": SQLiteAdapter,
    "mysql": MySQLAdapter,
    "postgres": PostgreSQLAdapter
}


class RelationalAdapter:
    """"""
    
    def __init__(self, database: str) -> None:
        self.adapter: interface.SQLAdapterInterface = adapter[database]()
        self.tables = {}
    
    def datatable(self, tablename: str):
        return DataTable(self.adapter, tablename)
    
    def backup(self):
        pass
    
    



__all__ = [
    'RelationalAdapter',
]
