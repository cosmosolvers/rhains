"""
DATABASE SETTINGS
"""

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

rhconf = {
    'server': {
        'secretkey': SERVER.get('SECRET_KEY'),
        'host': [host for host in SERVER.get('HOST')],
        'port': SERVER.get('PORT'),
        'cors': SERVER.get('CORS')
    },
    'databases': {
        item: {
            key.lower(): value
            for key, value in values.items()
        }
        for item, values in DATABASES.items()
    }
}
# chargé les configurations avec celui de l'utilisateur avant utilisation
