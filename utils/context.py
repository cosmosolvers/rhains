""""""
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
