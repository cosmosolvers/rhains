"""
DATABASE SETTINGS
"""
import os

PROJECT = {
    'NAME': 'rhains',
    'VERSION': '0.0.1',
    'AUTHOR': 'rhains',
    'EMAIL': 'victorvaddely@gmail.com',
    'PATH': os.path.dirname(os.path.abspath(__file__)),
}

SERVER = {
    'SECRET_KEY': '',
    'HOST': [
        '0.0.0.0',
        '127.0.0.1'
    ],
    'PORT': '8001',
    'CORS': [
        '127.0.0.1',
    ]
}

DATABASES = {
    'default': {
        # sqlite, mysql, postgres, mongo, arango
        'ENGINE': 'sqlite',
        'USER': 'rhains',
        'PWD': 'rhains',
        'HOST': '127.0.0.1',
        'PORT': '',
        'NAME': 'rhains.db'
    },
}

MEDIA = {
    'prefered': {
        'size': -1,
    },
    'img': {
        'local': True,
        'path': 'media/img',
        'url': '/media/img',
        'prefered': {
            'size': 1024 * 1024 * 2,
            'format': 'jpeg'
        }
    },
    'video': {
        'local': True,
        'path': 'media/video',
        'url': '/media/video',
        'prefered': {
            'size': 1024 * 1024 * 10,
            'format': 'mp4'
        }
    },
    'audio': {
        'local': True,
        'path': 'media/audio',
        'url': '/media/audio',
        'prefered': {
            'size': 1024 * 1024 * 5,
            'format': 'mp3'
        }
    },
    'file': {
        'local': True,
        'path': 'media/file',
        'url': '/media/file',
    }
}

FIELD_CONSTRAINTS = {
    
}

rhconf = {
    'project': {k.lower(): v for k, v in PROJECT},
    'server': {
        'secretkey': SERVER.get('SECRET_KEY'),
        'host': [host for host in SERVER.get('HOST')],
        'port': SERVER.get('PORT'),
        'cors': SERVER.get('CORS')
    },
    'databases': {
        item.lower(): {
            key.lower(): value
            for key, value in values.items()
        }
        for item, values in DATABASES.items()
    },
    'media': {
        item.lower(): {
            k.lower(): v
            for k, v in values.items()
        }
        for item, values in MEDIA.items()
    }
}
# chargé les configurations avec celui de l'utilisateur avant utilisation
