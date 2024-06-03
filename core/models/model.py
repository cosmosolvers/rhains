"""
"""


class Model:
    connexion = None

    def __repr__(self):
        return f"<{self.__tablename__} rhains object {self.pk}>"

    # sauvegarde un objet
    def save(self, *args, **kwargs):
        pass

    # supprime un objet
    def delete(self, *args, **kwargs):
        pass

    class Meta:
        database = 'default'
        abscratc = False
