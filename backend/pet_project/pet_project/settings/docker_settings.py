from corsheaders.defaults import default_headers

from .base import *  # pragma: no cover

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASES = {  # pragma: no cover
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

THIRD_PARTY_APPS += [  # pragma: no cover
    'corsheaders',
]

MIDDLEWARE += [  # pragma: no cover
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_EXPOSE_HEADERS = [
    'Content-Disposition', ]
CORS_ALLOW_CREDENTIALS = True  # pragma: no cover
CORS_ALLOW_ALL_ORIGINS = True
CACHES = {  # pragma: no cover
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': None,
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"  # pragma: no cover
SESSION_CACHE_ALIAS = "default"  # pragma: no cover

CACHE_TTL = 60 * 1  # pragma: no cover


logger_level = 'INFO'  # pragma: no cover
LOGGING = {  # pragma: no cover
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "console": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
    'handlers': {
        'console': {
            "level": logger_level,
            "class": "rq.utils.ColorizingStreamHandler",
            "formatter": "console",
            "exclude": ["%(asctime)s"],
        },
    },
    'root': {
        'handlers': ['console'],
        'level': logger_level,
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', logger_level),
            'propagate': False,
        },
    },
}

REDIS_HOST = os.environ.get('REDIS_HOST')  # pragma: no cover
REDIS_PORT = '6379'  # pragma: no cover