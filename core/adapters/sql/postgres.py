""""""

import psycopg2

from core.adapters.interface import SQLAdapterInterface





class PostgreSQLAdapter(SQLAdapterInterface):
        
        def connect(self, *args, **kwargs):
            """
            dbname: str,
            user: str,
            password: str,
            host: str,
            port: str
            """
            self.connection = psycopg2.connect(*args, **kwargs)
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
