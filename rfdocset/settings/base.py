"""
Django settings for rfdocset project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

_rfdocs_logs = os.path.join(BASE_DIR, 'logs', 'rfdocs')
_django_logs = os.path.join(BASE_DIR, 'logs', 'django')


for p in (_rfdocs_logs, _django_logs):
    if not os.path.exists(p):
        os.makedirs(p)


def get_env_variable(var, fail_to=None):
    """
    Gets the environment variable or returns exception
    """
    res = os.environ.get(var, fail_to)
    if not res:
        raise ImproperlyConfigured("Set the %s environment variable" % var)
    return res

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

TEMPLATE_STRING_IF_INVALID = "INVALID EXPRESSION: %s"

INTERNAL_IPS = ('127.0.0.1', )
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'django_extensions',
    'rest_framework',
    'compressor',  # requires 'compressor.finders.CompressorFinder' in STATICFILES_FINDERS
    'rfdocs',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'rfdocset.urls'

WSGI_APPLICATION = 'rfdocset.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rfdocs_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
    'test': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rfdocs_db_test',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': [
            'unix:/tmp/memcached_default.sock',
        ],
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    },
    'dataset': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': [
            'unix:/tmp/memcached_dataset.sock',
        ],
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format':
            '[%(asctime)s] %(levelname)s: %(module)s %(funcName)s {pid: %(process)d} {thr: %(thread)d} %(message)s',
            'datefmt': '%y/%b/%d %H:%M:%S',
        },
        'standard': {
            'format': '[%(asctime)s] %(levelname)s: %(module)s %(funcName)s %(message)s',
            'datefmt': '%y/%b/%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
            'datefmt': '%y/%b/%d %H:%M:%S',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'rfdocs', 'rfdocs.log'),
            'formatter': 'verbose',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 10
        },
        'django_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django', 'django.log'),
            'formatter': 'verbose',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 10
        },
        'django_requests_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django', 'requests.log'),
            'formatter': 'verbose',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 10
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins', 'django_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'django_requests_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'rfdocs.utils.downloaders.alternate.phantomjs': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'rfdocs.utils.downloaders.downloader': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'rfdocs.utils.parsers.base': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'rfdocs.mixins.memcached_helper': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'rfdocs.admin': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'rfdocs.models': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'rfdocs.views': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'rfdocs.views_api': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'mysite.forms': {
            'handlers': ['file', 'mail_admins', ],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',  # requires 'compressor' in INSTALLED_APPS
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'rfdocs', 'static'),
)

RFDOCS = {
    'MAX_FILE_SIZE': 5242880,
    'ALLOWED_CONTENT_TYPES': ['text/html', 'text/plain', 'text/richtext'],
    'FORCE_HTTP_IN_JSON_DATA': True,
    'PROJ_TITLE': 'Robot Framework Documentation',
    'PAGINATE_BY': 25
}

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

REST_FRAMEWORK = {
    'PAGINATE_BY': 1000
}

COMPRESS_ENABLED = True