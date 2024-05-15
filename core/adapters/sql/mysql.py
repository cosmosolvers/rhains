""""""

import MySQLdb

from core.adapters.interface import SQLAdapterInterface




class MySQLAdapter(SQLAdapterInterface):
    
    def connect(self, *args, **kwargs):
        """
        host: str,
        user: str,
        passwd: str,
        db: str,
        port: int
        """
        self.connection = MySQLdb.connect(*args, **kwargs)
        self.cursor = self.connection.cursor()
    
    def execute(self, query: str, values=None, fetch=False, commit=False, *args, **kwargs):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        
        if commit:
            self.connection.commit()
        
        if fetch:
            results = self.cursor.fetchall()
            return results
    
    def backup(self, filename: str):
        with open(filename, "w") as f:
            for line in self.connection.iterdump():
                f.write(f"{line}\n")
    
    def close(self):
        self.connection.close()
