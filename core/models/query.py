"""
"""

class Query:
    
    from .model import Model
    """
    """
    def __init__(self, model: Model):
        self.model = model
    
    # cree un nouvel objet
    def create(self, *args, **kwargs) -> Model:
        """
        """
        pass
    
    # sauvegarde un objet
    def save(self, *args, **kwargs) -> Model:
        pass
    
    # supprime un objet
    def delete(self, *args, **kwargs) -> Model:
        pass
    
    # met a jour un objet
    def update(self, *args, **kwargs) -> Model:
        pass
    
    # recupere un objet
    def get(self, *args, **kwargs) -> Model:
        pass
    
    # recupere tous les objets
    def all(self, *args, **kwargs) -> Model:
        pass
    
    # filtre les objets
    def filter(self, *args, **kwargs) -> Model:
        pass
    
    # exclut les objets
    def exclude(self) -> Model:
        pass
    
    # trie les objets
    def sort(self, *args, **kwargs) -> Model:
        pass
    
    # recupere les n premiers objets
    def limit(self, n: int=10, *args, **kwargs) -> Model:
        pass
    
    # saute les n premiers objets
    def skip(self, page: int=0, *args, **kwargs) -> Model:
        pass
    
    # compte les objets
    def count(self, *args, **kwargs) -> Model:
        pass
    
    # verifie si un objet existe
    def exists(self, *args, **kwargs) -> Model:
        pass
    
    # recupere les valeurs des objets
    def values(self, *args, **kwargs) -> Model:
        pass

    # recupere les objets distinctes
    def distinct(self, *args, **kwargs) -> Model:
        pass
    
    def aggregate(self, *args, **kwargs) -> Model:
        pass
    
    def extra(self) -> Model:
        pass
    
    def defer(self) -> Model:
        pass
    
    def using(self) -> Model:
        pass
    
    def get_or_create(self) -> Model:
        pass

    def update_or_create(self) -> Model:
        pass
    
    # recupere le premier objet
    def first(self) -> Model:
        pass
    
    # recupere le dernier objet
    def last(self) -> Model:
        pass
    
    # recupere une copie de l'objet
    def _clone(self) -> Model:
        pass



class Schema:
    """
    """
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
    
    # cree une nouvelle table
    def create(self, *args, **kwargs):
        pass
    
    # supprime une table
    def drop(self, *args, **kwargs):
        pass
    
    # modifie une table
    def alter(self, *args, **kwargs):
        pass
    
    # ajoute une colonne
    def add(self, *args, **kwargs):
        pass
    
    # supprime une colonne
    def remove(self, *args, **kwargs):
        pass
    
    # modifie une colonne
    def modify(self, *args, **kwargs):
        pass
    
    # renomme une colonne
    def rename(self, *args, **kwargs):
        pass
    
    # change une colonne
    def change(self, *args, **kwargs):
        pass
    
    # verifie si une colonne existe
    def exists(self, *args, **kwargs):
        pass
    
    def has(self, *args, **kwargs):
        pass
    
    def get(self, *args, **kwargs):
        pass
    
    def set(self, *args, **kwargs):
        pass

    def unset(self, *args, **kwargs):
        pass
    
    def default(self, *args, **kwargs):
        pass
    
    def primary(self, *args, **kwargs):
        pass
    
    def unique(self, *args, **kwargs):
        pass
    
    def index(self, *args, **kwargs):
        pass
    
    def foreign(self, *args, **kwargs):
        pass
    
    def check(self, *args, **kwargs):
        pass
    
    def references(self, *args, **kwargs):
        pass
    
    def on(self, *args, **kwargs):
        pass
    
    def to(self, *args, **kwargs):
        pass
    
    def cascade(self, *args, **kwargs):
        pass
    
    def restrict(self, *args, **kwargs):
        pass
    
    def noaction(self, *args, **kwargs):
        pass
    
    # recupere la table courante
    def setdefault(self, *args, **kwargs):
        pass
    
    def setnull(self, *args, **kwargs):
        pass
    
    # supprime la valeur par defaut de la colonne
    def setnone(self, *args, **kwargs):
        pass
    
    # recupere la table courante
    def setcurrent(self, *args, **kwargs):
        pass
