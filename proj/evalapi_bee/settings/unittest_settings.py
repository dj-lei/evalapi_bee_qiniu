import os

from .default import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # NOQA F405
    }
}


os.environ['EVLA_DB_SETTING'] = 'LOCAL'
