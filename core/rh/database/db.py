"""
CONFIGURATION LOADING
"""
from utils.context import get_models_from_package_or_module
from utils.attrs import Attributes

from core.models.model import Model
from core.config.conf import rhconf
from core.rh.connection import Connection

from typing import Dict


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


def create_table(models, connection, collection):
    """"""
    print('=== NEW DATABASE TABLE SEARCH ===')
    for model in models:
        data = getattr(collection, model.__name__.lower())
        connect = connection(
            model=data.model,
            engine=data.engine,
            session=data.session
        )
        connect.table()


def alter_table(models, connection, collection):
    for model in models:
        data = getattr(collection, model.__name__.lower())
        connect = connection(
            model=data.model,
            engine=data.engine,
            session=data.session
        )
        connect.alter()


class Databases:
    def __init__(self, model_path) -> None:
        # recuperons les databases
        self.__databases: Dict = rhconf['database']
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
            engine = self.__databases.get('database').get('engine')
            self.__collection[name] = {
                'model': model,
                'engine': engine,
                'session': session_manager.get_connexion(database)
            }
        self.__collection = Attributes(**self.__collection)
        # creation des tables
        create_table(models, Connection, self.__collection)
        # ajouter les modification
        alter_table(models, Connection, self.__collection)

    def __getitem__(self, name: str) -> Connection | None:
        collection = getattr(self.__collection, name)
        if not collection:
            return None
        return Connection(
            model=collection.model,
            engine=collection.engine,
            session=collection.connect
        )

    def __register(self, name: str, dbconf: Dict) -> None:
        engine = dbconf.get('engine')
        connexion = adaptor.get(engine)(**dbconf)
        session_manager.register(name, connexion)
