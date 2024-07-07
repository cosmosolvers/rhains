""""""
from core.models.model import Model


def pk(*args):
    for arg in args:
        if isinstance(arg, Model) or issubclass(arg, Model):
            arg = getattr(arg, arg.Meta.pk)


def instance(self, *args):
    for arg in args:
        if issubclass(arg, Model):
            pk = arg.Meta.pk
            if not self.get({pk: getattr(arg, pk)}):
                raise ValueError(f"this instance for {arg.__class__.__name__} not exists")
