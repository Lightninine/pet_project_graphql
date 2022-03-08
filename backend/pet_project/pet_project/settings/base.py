import os
from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '10.3.29.23', '82.138.49.100', 'localhost',
                 'act.robdrill.tech', '26.9.127.21']
ALLOWED_HOSTS += [f'192.168.{i}.{j}' for i in range(256) for j in range(256)]
# Application definition

DJANGO_APPS = [

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'memoize',
    "graphql_auth",
    'channels',
    'channels_redis',
    "graphene_django",
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    'django_cleanup.apps.CleanupConfig',
    'django_filters'
]

LOCAL_APPS = [
    'users.apps.UsersConfig',
    'core',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',

]

ROOT_URLCONF = 'pet_project.urls'

AUTH_USER_MODEL = "users.CustomUser"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'pet_project.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ASGI_APPLICATION = 'pet_project.asgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': None,
    }
}


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
MEDIA_ROOT = 'media'
# STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'staticfiles'),
#    ]

GRAPPELLI_INDEX_DASHBOARD = \
    'dashboard.CustomIndexDashboard'
LOGIN_REDIRECT_URL = 'profile'
LOGIN_URL = '/api/token/obtain/'