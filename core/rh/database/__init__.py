"""databse connection adapter"""

from .adapter import Adapter
from .root.sqlite import (
    SqliteAdapter, SqliteCRUD, SqliteDatacrud, SqliteTablecrud
)
from .root.mysql import (
    MysqlAdapter, MysqlDatacrud, MysqlTablecrud, MysqlCRUD
)
from .root.postgres import (
    PostgresAdapter, PostgresCRUD, PostgresDatacrud, PostgresTablecrud
)
from .root.mongodb import (
    MongoDBAdapter, MongoDBCRUD, MongoDBDatacrud, MongoDBTablecrud
)
from .root.arangodb import (
    ArangoDBAdapter, ArangoDBCRUD, ArangoDBDatacrud, ArangoDBTablecrud
)


__all__ = [
    'SqliteAdapter',
    'SqliteCRUD',
    'SqliteDatacrud',
    'SqliteTablecrud',

    'MysqlAdapter',
    'MysqlDatacrud',
    'MysqlCRUD',
    'MysqlTablecrud',

    'PostgresAdapter',
    'PostgresCRUD',
    'PostgresDatacrud',
    'PostgresTablecrud',

    'MongoDBAdapter',
    'MongoDBCRUD',
    'MongoDBDatacrud',
    'MongoDBTablecrud',

    'ArangoDBAdapter',
    'ArangoDBCRUD',
    'ArangoDBDatacrud',
    'ArangoDBTablecrud',

    'Adapter'
]
