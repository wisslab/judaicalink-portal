"""
Django settings for labs project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import logging

import environ
import os
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    EMAIL_USE_TLS=(bool,False),
    EMAIL_USE_SSL=(bool, False),
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# False if not in os.environ because of casting above
DEBUG = env('DEBUG')

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

ALLOWED_HOSTS = [
    'labs.judaicalink.org',
    'localhost',
    'judaicalink.org',
]+env('ALLOWED_HOSTS', default=[])

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'core',
    'backend.apps.BackendConfig',
    'search',
    'cm_search',
    'cm_e_search',
    'lodjango',
    'dashboard',
    'data',
    'crispy_forms',
    'captcha',
    'hcaptcha',
    'active_link',
    'environ',
    "crispy_bootstrap5",
    'cookiebanner',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'labs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
             os.path.join(BASE_DIR, 'templates'),
            ],
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

WSGI_APPLICATION = 'labs.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    #
    # The db() method is an alias for db_url().
    'default': env.db(),

    # read os.environ['SQLITE_URL']
    'extra': env.db_url(
        'SQLITE_URL',
        default='sqlite:///db.sqlite3'
    )
}

# Cache Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('REDIS_URL') if env('REDIS_URL') is not None else 'redis://localhost:6379',
    },
 }
CACHE_TTL = 60 * 15

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = env('STATIC_ROOT') if env('STATIC_ROOT') is not None else os.path.join(BASE_DIR, "static/")

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {  # VerboseFormatter
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
            'style': '%',
        },
        'simple': {  # SimpleFormatter
            'format': '%(levelname)s %(message)s',
            'style': '%',
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': env('LOGFILE') if env('LOGFILE') is not None else os.path.join(BASE_DIR, 'logs/labs.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'labs': {
            'handlers': ['logfile', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Crispy form
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email settings
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_TO = env('EMAIL_TO')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_USE_SSL = env('EMAIL_USE_SSL')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')


# Channels
ASGI_APPLICATION = "labs.routing.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# labs settings
LABS_ROOT = env('LABS_ROOT') if env('LABS_ROOT') is not None else 'http://localhost:8000'
LABS_GIT_WEBROOT = env('LABS_GIT_WEBROOT') if env('LABS_GIT_WEBROOT') is not None else "https://github.com/wisslab/judaicalink-labs/blob/master/labs/"
LABS_DUMPS_WEBROOT = env('LABS_DUMPS_WEBROOT') if env('LABS_DUMPS_WEBROOT') is not None else "http://data.judaicalink.org/dumps/"
LABS_DUMPS_LOCAL = env('LABS_DUMPS_LOCAL') if env('LABS_DUMPS_LOCAL') is not None else "dumps/"

# Fuseki
FUSEKI_SERVER = env('FUSEKI_SERVER') if env('FUSEKI_SERVER') is not None else "http://localhost:3030"
FUSEKI_STORAGE = env('FUSEKI_STORAGE') if env('FUSEKI_STORAGE') is not None else "."


# Elasticsearch
#ELASTICSEARCH_SERVER = "https://localhost:9200/" if env('ELASTICSEARCH_SERVER') is None else env('ELASTICSEARCH_SERVER')
#ELASTICSEARCH_STORAGE = "/var/lib/elasticsearch"
#ELASTICSEARCH_SSL_ENABLED = False if ELASTICSEARCH_SERVER.startswith("http://") else True
#ELASTICSEARCH_USER = "elastic" if env('ELASTICSEARCH_USER') is None else env('ELASTICSEARCH_USER')
#ELASTICSEARCH_PASSWORD = None if env('ELASTICSEARCH_PASSWORD') is None else env('ELASTICSEARCH_PASSWORD')
JUDAICALINK_INDEX = env('JUDAICALINK_INDEX') if env('JUDAICALINK_INDEX') is not None else "judaicalink"
COMPACT_MEMORY_INDEX = env('COMPACT_MEMORY_INDEX') if env('COMPACT_MEMORY_INDEX') is not None else "cm"
COMPACT_MEMORY_META_INDEX = env('COMPACT_MEMORY_META_INDEX') if env('COMPACT_MEMORY_META_INDEX') is not None else "cm_meta"

# Solr
SOLR_SERVER = env('SOLR_SERVER') if env('SOLR_SERVER') is not None else "http://localhost:8983/solr"
SOLR_USER = env('SOLR_USER') if env('SOLR_USER') is not None else "solr"
SOLR_PASSWORD = env('SOLR_PASSWORD') if env('SOLR_PASSWORD') is not None else "solr"
SOLR_STORAGE = "/opt/solr"


# HCaptcha
HCAPTCHA_SITEKEY = env('HCAPTCHA_SITEKEY')
HCAPTCHA_SECRET = env('HCAPTCHA_SECRET')

HCAPTCHA_DEFAULT_CONFIG = {
    'onload': 'name_of_js_function',
    'render': 'explicit',
    'theme': 'light',  # do not use data- prefix
    'size': 'normal',  # do not use data- prefix
}


# if the settings in the .env contain the ELASTICSEARCH_SERVER_CERT_PATH use it, else throw an error
#if ELASTICSEARCH_SSL_ENABLED and env('ELASTICSEARCH_SERVER_CERT') is not None:
#    ELASTICSEARCH_SERVER_CERT = env('ELASTICSEARCH_SERVER_CERT')
#else:
#    logging.ERROR("ELASTICSEARCH_SERVER_CERT_PATH not set in .env file")
#    raise Exception('ELASTICSEARCH_SERVER_CERT_PATH not set in .env')

# Geonames
# https://www.geonames.org/login
GEONAMES_API_USER = env('GEONAMES_API_USER') if env('GEONAMES_API_USER') is not None else ""

# Django Cookie Banner
COOKIEBANNER = {
    "title": _("Cookie settings"),
    "header_text": _("We are using cookies on this website. A few are essential, others are not."),
    "footer_text": _("Please accept our cookies"),
    "footer_links": [
        {"title": _("Imprint"), "href": "/imprint"},
        {"title": _("Privacy"), "href": "/privacy"},
    ],
    "groups": [
        {
            "id": "essential",
            "name": _("Essential"),
            "description": _("Essential cookies allow this page to work."),
            "cookies": [
                {
                    "pattern": "cookiebanner",
                    "description": _("Meta cookie for the cookies that are set."),
                },
                {
                    "pattern": "csrftoken",
                    "description": _("This cookie prevents Cross-Site-Request-Forgery attacks."),
                },
                {
                    "pattern": "sessionid",
                    "description": _("This cookie is necessary to allow logging in, for example."),
                },
            ],
        },
        {
            "id": "analytics",
            "name": _("Analytics"),
            "optional": True,
            "cookies": [
                {
                    "pattern": "_pk_.*",
                    "description": _("Matomo cookie for website analysis."),
                },
            ],
        },
    ],
}

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://judaicalink.org',
    'https://labs.judaicalink.org',
    'https://www.judaicalink.org',
    'https://web.judaicalink.org',
    'https://data.judaicalink.org',
]

CSRF_FAILURE_VIEW = 'contact.views.csrf_failure'

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')