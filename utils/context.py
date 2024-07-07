"""
changement a faire

regardez que dans models
- si models est un package regardez uniquement dans son fichier __init__.py
- sinon uniquement dans models.py

conclusion
==========

les developpeur qui fond de models un package doivent
importer tout les models dans __init__.py du package models
"""
import pkgutil


# recherche tout les class heritant de facon direct ou indirect de la classe
# Model dans le fichiers au package dont le nom est entré en paramtere
def get_models_from_package_or_module(path: str, model_class: type) -> list:
    models = []
    for importer, modname, ispkg in pkgutil.iter_modules([path]):
        module = importer.find_module(modname).load_module(modname)
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, model_class):
                models.append(obj)
    return models


def primarykeys(model) -> str:
    for field, module in model.mapping:
        if module._primarykey:
            return field
    return None


def verifykeys(model):
    count = 0
    for k, v in model.mapping:
        if v._primarykey:
            count += 1
    if count != 1:
        raise AttributeError('too many field are primary key')
