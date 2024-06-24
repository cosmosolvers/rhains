"""
CONFIGURATION LOADING
"""
from utils.context import get_models_from_package_or_module
from core.models.model import Model

from typing import Dict

from ..collection import Connection
from ..session import session_manager
from ..database import (
    SqliteAdapter,
    PostgresAdapter,
    MysqlAdapter,
    MongoDBAdapter,
    ArangoDBAdapter
)


adaptor = {
    'sqlite': SqliteAdapter,
    'mysql': MysqlAdapter,
    'postgres': PostgresAdapter,
    'mongodb': MongoDBAdapter,
    'Arangodb': ArangoDBAdapter
}


class Databases:
    def __init__(self, rhconf: Dict, model_path) -> None:
        # recuperons les databases
        self.__databases: Dict = rhconf.get('databases')
        # enregistrons les connexion
        for name, dbconf in self.__databases.items():
            self.__register(name, dbconf)
        # recuperons les tables
        models = [
            model for model
            in get_models_from_package_or_module(model_path, Model)
            if not model.Meta.abstract
        ]
        # creons notre collection
        self.__collection = {}
        for model in models:
            name = str(model.__name__).lower()
            database = model.Meta.database
            engine = self.__databases[database]['engine']
            self.__collection[name] = {
                'model': model,
                'engine': engine,
                'connect': session_manager.get_connexion(database)
            }

    def __getitem__(self, key: str) -> Dict:
        if key in self.__tables.keys():
            return Connection(**self.__tables[key])

    def __register(self, name: str, dbconf: Dict) -> None:
        engine = dbconf.get('engine')
        connexion = adaptor.get(engine)(**dbconf)
        session_manager.register(name, connexion)
