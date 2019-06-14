from .default import *  # NOQA


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pingjia",
        "USER": "pingjia",
        "PASSWORD": "De32wsxC",
        "HOST": "192.168.2.114",
        "PORT": "3306"
    }
    # 'kong': {
    #     "ENGINE": "django.db.backends.postgresql_psycopg2",
    #     "NAME": "kong",
    #     "USER": "gpj_dbuser",
    #     "PASSWORD": "TEST_249_dbuser",
    #     "HOST": "101.200.229.249",
    #     "PORT": "5432"
    # }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # multiple memcached server
        'LOCATION': '192.168.1.187:11211',
        'TIMEOUT': 61200,  # 07-24 17 hours
        'BINARY': True,
        'KEY_PREFIX': 'EVALAPI.1'
    },
    'file_cache': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/wwwcache',  # Set file cache directory
        'TIMEOUT': 61200,  # 07-24 17 hours
        'KEY_PREFIX': 'EVALAPI.1',
        'OPTIONS': {
            'MAX_ENTRIES': 100000,
            'CULL_FREQUENCY': 3,
        }
    },
}

LOGGING['loggers']['django.db.backends'] = {
    'level': 'DEBUG',
    'filters': ['require_debug_true'],
    # 'handlers': ['console'],
}

DEBUG = True
ALLOWED_HOSTS = ['*']


INSTALLED_APPS += [
    'fixture_magic',
    'debug_toolbar'
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'deal_records.utils.NonHtmlDebugToolbarMiddleware',
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

INTERNAL_IPS = ('127.0.0.1', )