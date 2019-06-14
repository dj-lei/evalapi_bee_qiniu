import os

from corsheaders.defaults import default_headers

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'kw18yxz*#qn8=ps**#p4gh&)bw5+rfq(ebu+))=2wmo30h&*gn'

DEBUG = False

# ALLOWED_HOSTS = ['.gongpingjia.com', '.alicontainer.com', 'evalapi_bee']
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = ()
CORS_ALLOW_HEADERS = default_headers + (
    'verify-resourse',
    'verify-resource',
    'app-version',
    'x-gpj-response-style',
    'x-gpj-request-id'
)

SESSION_COOKIE_NAME = 'evalapi_bee_sessionid'

CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'khas_core.django_jwt',
    'raven.contrib.django.raven_compat',
    'corsheaders',

    'evalapi',
    'category',
    'general',
    'deal_records'
]

MIDDLEWARE = [
    'log_request_id.middleware.RequestIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'khas_core.csrf.middleware.DisableCSRF',
    'khas_core.django_jwt.middleware.JWTAuthenticationMiddleware',
    'khas_core.django_jwt.middleware.JWTCookieMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'evalapi_bee.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'evalapi_bee.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # NOQA E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # NOQA E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # NOQA E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # NOQA E501
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

JWT_SECRET = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
JWT_COOKIE_DOMAIN = '.gongpingjia.com'
JWT_COOKIE_NAME = 'auth_token'
JWT_COOKIE_AGE = 864000
JWT_COOKIE_PATH = '/'
JWT_COOKIE_SECURE = False
JWT_COOKIE_HTTPONLY = True
JWT_EXPIRE_TIME = 864300
JWT_USER_FIELDS = ('id', 'username', 'is_staff')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'DATETIME_FORMAT': '%s.%f',
    'EXCEPTION_HANDLER': 'khas_core.rest.views.exception_handler',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',)
}

RAVEN_CONFIG = {
    # 'dsn': '',  # TODO
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] [%(name)s] [%(request_id)s] [%(threadName)s:%(thread)d] [%(asctime)s] [%(module)s:%(lineno)d]: %(message)s'
        }
    },
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'queries_above_500ms': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.duration > 0.5 if hasattr(record, 'duration') else False
        },
        # 'log_all_queries': {
        #     '()': 'django.utils.log.CallbackFilter',
        #     'callback': a                   # 打开这个选项来打印所有sql查询
        # }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filters': ['request_id'],
            'filename': os.path.join(BASE_DIR, "../../logs", "common.log"),
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['request_id'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'django.test': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "pingjia",
#         "USER": "pingjia",
#         "PASSWORD": "De32wsxC",
#         "HOST": "100.114.30.239",
#         "PORT": "18056",
#         "STORAGE_ENGINE": "INNODB",
#         "OPTIONS": {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     },
#     'kong': {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": "kong",
#         "USER": "gpj_dbuser",
#         "PASSWORD": "pg_GPJ_~!",
#         "HOST": "10.24.197.91",
#         "PORT": "5432"
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pingjia",
        "USER": "pingjia",
        "PASSWORD": "De32wsxC",
        "HOST": "192.168.2.114",
        "PORT": "3306"
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         # multiple memcached server
#         'LOCATION': '93d98b389c094fd7.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211',
#         'TIMEOUT': 61200,  # 07-24 17 hours
#         'BINARY': True,
#         'KEY_PREFIX': 'EVALAPI.1'
#     },
#     'file_cache': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/tmp/wwwcache',  # Set file cache directory
#         'TIMEOUT': 61200,  # 07-24 17 hours
#         'KEY_PREFIX': 'EVALAPI.1',
#         'OPTIONS': {
#             'MAX_ENTRIES': 100000,
#             'CULL_FREQUENCY': 3,
#         }
#     },
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # multiple memcached server
        'LOCATION': '127.0.0.1:11211',
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

# import threading

# t = threading.current_thread()
# if t.name != 'Main Thread':

