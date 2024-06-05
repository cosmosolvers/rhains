"""
"""

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
