import os
import dj_database_url
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
CAMPAIGN_ID = 1
USE_I18N = True
MEDIA_URL = '/site-media/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMIN_MEDIA_PREFIX = '/admin-media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'json_field',
    'main',
)

#database
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

# Absolute path to the directory that holds media.
MEDIA_ROOT = PROJECT_DIR + '/media'
ADMIN_MEDIA_ROOT = PROJECT_DIR + '/media'

# templates
TEMPLATE_DIRS = (
    PROJECT_DIR + "/templates"
)

#admins
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

SLEEP_BETWEEN_TWEETS = 60
BASE_URL = 'http://radar.brixtonbuzz.com'

try:
    TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
    TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
    TWITTER_ACCESS_TOKEN_KEY = os.environ['TWITTER_ACCESS_TOKEN_KEY']
    TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
except KeyError:
    pass

try:
    from local_settings import *
except ImportError:
    pass
