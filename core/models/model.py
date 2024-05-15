"""
"""
from rhains.core.models.query import Query


# pip install
import shortuuid



class Model:
    """
    """
    query : Query = None
    __tablename__ : str = None
    _id: str = shortuuid.uuid()
    _meta = {
        'database': 'default'
    }

    def __init__(self, *args, **kwargs):
        self.__tablename__ = self.__class__.__name__
        self.query = Query(self.__tablename__.lower())

    def __repr__(self):
        return f"<{self.__tablename__} object {self._id}>"
