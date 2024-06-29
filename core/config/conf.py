"""
DATABASE SETTINGS
"""
import os
import secrets
from typing import Dict, Any


__project = {
    'name': '',
    'version': '0.0.1',
    'author': '',
    'email': '',
    'path': os.path.dirname(os.path.abspath(__file__))
}

__server = {
    'secret_key': 'rhains_' + str(secrets.token_hex(64)),
    'host': ['0.0.0.0', '127.0.0.1'],
    'port': 8001,
    'cors': ['127.0.0.1']
}

__databases = {
    # sqlite, mysql, postgres, mongo, arango
    'root': {
        'engine': 'sqlite',
        'user': '',
        'host': '127.0.0.1',
        'name': 'rhains.sqlite3',
        'port': 8000,
        'pwd': ''
    }
}

__media = {
    'file': {
        'local': True,
        'path': 'media/',
        'url': '',
        'prefered': {
            'size': -1,
            'format': ''
        }
    }
}

configure = {
    'project': __project,
    'server': __server,
    'database': __databases,
    'media': __media
}


def verify_dict(data, value):
    for k, v in data.items():
        if k not in value:
            value[k] = v
        elif isinstance(v, dict) and isinstance(value.get(k), dict):
            verify_dict(v, value.get(k))
        else:
            raise ValueError(f"{value} invalid!!!")


class Attrs:
    def __init__(self, **kwargs) -> None:
        if not kwargs:
            raise ValueError(f'{kwargs} cannot be null')
        self.__attrs(kwargs)
        self.__name = None

    def __set_name__(self, owner, name):
        self.__name = name

    def __set__(self, instance, value: Dict):
        if not instance.__dict__.get(self.__name):
            raise AttributeError('invalid action')
        # completer les parametre ohmis par l'utilisateur
        if self.__name in configure:
            verify_dict(configure.get(self.__name), value)
        self.__attrs(value)

    def __attrs(self, value: Dict):
        for k, v in value.items():
            if isinstance(v, dict):
                attrs = Attrs(**v)
                setattr(self, k, attrs)
            else:
                setattr(self, k, v)

    def __getattr__(self, name: str) -> Any:
        return self.__dict__.get(name)


class __RHConfig:
    def __init__(self, **kwargs) -> None:
        self.__conf = Attrs(**kwargs)

    def __getattr__(self, name: str) -> Any:
        if hasattr(self.__conf, name):
            return getattr(self.__conf, name)
        return None

    def __setattr__(self, name: str, value: Any) -> None:
        if name == '_RHConfig__conf':
            super().__setattr__(name, value)
        elif hasattr(self.__conf, name):
            attr = getattr(self.__conf, name)
            if isinstance(attr, Attrs) and isinstance(value, dict):
                verify_dict(configure.get(name), value)
            attr = Attrs(**value)
            setattr(self.__conf, name, attr)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __get__(self, instance, owner) -> Attrs:
        if instance is None:
            return self
        return self.__conf


rhconf = __RHConfig(**configure)


__all__ = ['rhconf']

# MEDIA = {
#     'prefered': {
#         'size': -1,
#     },
#     'img': {
#         'local': True,
#         'path': 'media/img',
#         'url': '/media/img',
#         'prefered': {
#             'size': 1024 * 1024 * 2,
#             'format': 'jpeg'
#         }
#     },
#     'video': {
#         'local': True,
#         'path': 'media/video',
#         'url': '/media/video',
#         'prefered': {
#             'size': 1024 * 1024 * 10,
#             'format': 'mp4'
#         }
#     },
#     'audio': {
#         'local': True,
#         'path': 'media/audio',
#         'url': '/media/audio',
#         'prefered': {
#             'size': 1024 * 1024 * 5,
#             'format': 'mp3'
#         }
#     },
#     'file': {
#         'local': True,
#         'path': 'media/file',
#         'url': '/media/file',
#     }
# }

# # chargé les configurations avec celui de l'utilisateur avant utilisation
# rhconf = {
#     'project': {k.lower(): v for k, v in PROJECT.items()},
#     'server': {
#         'secretkey': SERVER.get('SECRET_KEY'),
#         'host': [host for host in SERVER.get('HOST')],
#         'port': SERVER.get('PORT'),
#         'cors': SERVER.get('CORS')
#     },
#     'databases': {
#         item.lower(): {
#             key.lower(): value
#             for key, value in values.items()
#         }
#         for item, values in DATABASES.items()
#     },
#     'media': {
#         item.lower(): {
#             k.lower(): v
#             for k, v in values.items()
#         }
#         for item, values in MEDIA.items()
#     }
# }
# # chargé les configurations avec celui de l'utilisateur avant utilisation
