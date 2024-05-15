""""""

from typing import List
from core.adapters import interface
from core.adapters.sql.sqlite import SQLAdapter
from core.adapters.sql.mysql import MySQLAdapter
from core.adapters.sql.postgres import PostgreSQLAdapter



adapter = {
    "sqlite": SQLAdapter,
    "mysql": MySQLAdapter,
    "postgres": PostgreSQLAdapter
}



class DataTable:
    """"""
    
    def __init__(self, adapter: interface.SQLAdapterInterface, tablename: str) -> None:
        self.adapter = adapter
        self.tablename: str = tablename
    
    def exists(self):
        query = f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{self.tablename}'"""
        result = self.adapter.execute(query, fetch=True)
        return True if result else False
    
    def create(self, columns: List[str]):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.tablename} (
            {', '.join(columns)}
        )
        """
        self.adapter.execute(query, commit=True)
    
    def insert(self, values: List[str]):
        query = f"""INSERT INTO {self.tablename} VALUES ({', '.join(["?"] * len(values))})"""
        self.adapter.execute(query, values, fetch=True, commit=True)
    
    def select(
        self,
        limit: int=-1,
        where: str=None,
        order_by: str=None,
        join: bool=False
    ):
        query = f"""
            SELECT * FROM {self.tablename}
            {f"WHERE {where}" if where else ""}
        """
        results = self.adapter.execute(query, fetch=True)
        return results
    
    def delete(self, where=None):
        query = f"""
            DELETE FROM {self.tablename}
            {f"WHERE {where}" if where else ""}
        """
        self.adapter.execute(query, commit=True)
    
    def update(self, values: List, where=None):
        query = f"""
            UPDATE {self.tablename}
            SET {', '.join([f"{column} = ?" for column in values])}
            {f"WHERE {where}" if where else ""}
        """
        self.adapter.execute(query, values, commit=True)
    
    def drop(self):
        query = f"DROP TABLE IF EXISTS {self.tablename}"
        self.adapter.execute(query, commit=True)
    
    def truncate(self):
        query = f"TRUNCATE TABLE {self.tablename}"
        self.adapter.execute(query, commit=True)
    
    def count(self):
        query = f"SELECT COUNT(*) FROM {self.tablename}"
        result = self.adapter.execute(query, fetch=True)
        return result[0][0]
    
    def __repr__(self) -> str:
        return f"<DataTable {self.tablename}>"
    
    



class SQLMapper:
    """"""
    
    def __init__(self, database: str) -> None:
        self.adapter = adapter[database]()
        self.tables = {}
    
    def datatable(self, tablename: str):
        return DataTable(self.adapter, tablename)
    
    def backup(self):
        pass
