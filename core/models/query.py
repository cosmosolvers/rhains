"""
"""

class Query:
    """
    """
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
    
    # cree un nouvel objet
    def create(self, *args, **kwargs):
        pass
    
    # sauvegarde un objet
    def save(self, *args, **kwargs):
        pass
    
    # supprime un objet
    def delete(self, *args, **kwargs):
        pass
    
    # met a jour un objet
    def update(self, *args, **kwargs):
        pass
    
    # recupere un objet
    def get(self, *args, **kwargs):
        pass
    
    # recupere tous les objets
    def all(self, *args, **kwargs):
        pass
    
    # filtre les objets
    def filter(self, *args, **kwargs):
        pass
    
    # exclut les objets
    def exclude(self):
        pass
    
    # ordonne les objets
    def order(self, *args, **kwargs):
        pass
    
    # trie les objets
    def sort(self, *args, **kwargs):
        pass
    
    # recupere les n premiers objets
    def limit(self, n: int=10, *args, **kwargs):
        pass
    
    # saute les n premiers objets
    def skip(self, page: int=0, *args, **kwargs):
        pass
    
    # compte les objets
    def count(self, *args, **kwargs):
        pass
    
    # verifie si un objet existe
    def exists(self, *args, **kwargs):
        pass
    
    # recupere les valeurs des objets
    def values(self, *args, **kwargs):
        pass

    # recupere les objets distinctes
    def distinct(self, *args, **kwargs):
        pass
    
    def aggregate(self, *args, **kwargs):
        pass
    
    # recupere les elements de la ligne au champ specifie
    def raw(self, *args, **kwargs):
        pass
    
    def extra(self):
        pass
    
    def defer(self):
        pass
    
    def using(self):
        pass
    
    def get_or_create(self):
        pass
    
    # recupere le premier objet
    def first(self):
        pass
    
    # recupere le dernier objet
    def last(self):
        pass
    
    # recupere une copie de l'objet
    def _clone(self):
        pass

