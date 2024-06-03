""""""

import sqlite3

from core.adapters.interface import SQLAdapterInterface





class SQLiteAdapter(SQLAdapterInterface):
    
    def connect(self, *args, **kwargs):
        try:
            self.connection = sqlite3.connect(*args, **kwargs)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise DatabaseConnectionError(e)
    
    def execute(self, query: str, values=None, fetch=False, commit=False, *args, **kwargs):
        
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)

            if commit:
                self.connection.commit()

            if fetch:
                results = self.cursor.fetchall()
                return results
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            raise DatabaseExecutionError(e)
    
    def backup(self, filename: str):
        with open(filename, "w") as f:
            for line in self.connection.iterdump():
                f.write(f"{line}\n")
    
    def close(self):
        self.connection.close()
