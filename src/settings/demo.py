# -*- coding: utf-8 -*-

import os
from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, 'demo.sqlite'), # Or path to database file if using sqlite3.
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    },
    # Uncomment and fill in if you want to sync this map with other ones
    #'other': {
    #    'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    #    'NAME': os.path.join(PROJECT_ROOT, 'other.sqlite'), # Or path to database file if using sqlite3.
    #    'USER': '',                             # Not used with sqlite3.
    #    'PASSWORD': '',                         # Not used with sqlite3.
    #    'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
    #    'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    #},
}

# Uncomment if you want to sync this map with other ones
#INSTALLED_APPS.append('macadjan_sync')

# People that get error notification emails
ADMINS = (
    ('Demo User', 'demo_user@demo.com'),
)

# People that get broken-link notification emails if SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = "demo_user@demo.com"
SERVER_EMAIL = 'demo_user@demo.com'

TIME_ZONE = 'Europe/Madrid'
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

# Skin for demo site
TEMPLATE_DIRS += (
    os.path.join(PROJECT_ROOT, 'skins/demo/templates'),
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'skins/demo/static'),
)

# Piwik settings
# If you want web traffic tracking with Piwik, enter here the host and site id
PIWIK_HOST = ''
PIWIK_SITE_ID = 0

# Default marker image (used for categories or subcategories that not define their own marker).
DEFAULT_MARKER_URL = 'img/markers/icons/cluster3.png'

# Whoosh index directory
HAYSTACK_CONNECTIONS['default']['PATH'] = os.path.join(PROJECT_ROOT, 'whoosh/index_demo')

