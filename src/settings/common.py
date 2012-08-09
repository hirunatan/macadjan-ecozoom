# -*- coding: utf-8 -*-

from os.path import join, realpath, dirname, exists
import os, django

PROJECT_ROOT = join(dirname(realpath(__file__)), '..')

USE_ETAGS = False
DEBUG = True
PREPEND_WWW = False
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = False # set to True if you want to receive an email whenever a 404 (not found) error
                                # is generated due to a broken link (not a hand typed url)

DEFAULT_CONTENT_TYPE = "text/html"

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#    }
#}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SESSION_ENGINE='django.contrib.sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_AGE = 1209600

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

USE_I18N = True
USE_L10N = True
USE_TZ = False

MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
)

SITE_ID = 1

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    "django.contrib.messages.context_processors.messages",
    'macadjan_ecozoom.context_processors.current_site_info',
    'macadjan_ecozoom.context_processors.is_sync_installed',
    'macadjan_ecozoom.context_processors.piwik_settings',
]

ROOT_URLCONF = 'urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.webdesign',
    'django.contrib.sites',
    'treemenus',
    'rosetta',
    'haystack',
#    'djcelery',
    'captcha',
    'south',
    'macadjan_importer',
    'macadjan_ecozoom',
    'macadjan',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s:%(module)s:%(process)d:%(message)s'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends':{
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'default':{
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

if not hasattr(globals(), 'SECRET_KEY'):
    SECRET_FILE = join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        from random import choice
        import string
        symbols = ''.join((string.lowercase, string.digits,
                                            string.punctuation ))
        SECRET_KEY = ''.join([choice(symbols) for i in range(50)])

        secret = file(SECRET_FILE, 'w')
        secret.write(SECRET_KEY)
        secret.close()

# Rosetta config

ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = False
ROSETTA_WSGI_AUTO_RELOAD = True

# Haystack config

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'whoosh'),
    },
}
HAYSTACK_DEFAULT_OPERATOR = 'AND'

# Django debug toolbar config
if DEBUG:
    try:
        import debug_toolbar
        MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware',]
        INTERNAL_IPS = ('127.0.0.1',)
        INSTALLED_APPS += ['debug_toolbar',]
        DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False,
        }
        DEBUG_TOOLBAR_PANELS = (
            'debug_toolbar.panels.version.VersionDebugPanel',
            'debug_toolbar.panels.timer.TimerDebugPanel',
            'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
            'debug_toolbar.panels.headers.HeaderDebugPanel',
            'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
            'debug_toolbar.panels.template.TemplateDebugPanel',
            'debug_toolbar.panels.sql.SQLDebugPanel',
            'debug_toolbar.panels.signals.SignalDebugPanel',
            'debug_toolbar.panels.logger.LoggingPanel',
        )
    except ImportError:
        pass

