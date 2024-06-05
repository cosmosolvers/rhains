"""databse connection adapter"""

from .adapter import Adapter
from .sqlite import (
    SqliteAdapter, SqliteCRUD, SqliteDatacrud, SqliteTablecrud
)
from .mysql import (
    MysqlAdapter, MysqlDatacrud, MysqlTablecrud, MysqlCRUD
)
from .postgres import (
    PostgresAdapter, PostgresCRUD, PostgresDatacrud, PostgresTablecrud
)
from .mongodb import (
    MongoDBAdapter, MongoDBCRUD, MongoDBDatacrud, MongoDBTablecrud
)
from .arangodb import (
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
