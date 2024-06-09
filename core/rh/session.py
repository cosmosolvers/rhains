from contextlib import contextmanager
from .database.adapter import Adapter


@contextmanager
def session(database: Adapter):
    database.connect()
    try:
        yield database.connexion
    finally:
        database.close()


class SessionManager:
    def __init__(self, *args, **kwargs):
        self.connexions = {}

    # def __enter__(self):
    #     self._connection = self._database.connect()
    #     return self._connection

    def register(self, name, connexion):
        self.connexions[name] = connexion

    def get_connexion(self, name):
        if name not in self.connexions.keys():
            raise ValueError(f"Database {name} not found")
        return self.connexions.get(name)

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self._connection.close()


session_manager = SessionManager()
