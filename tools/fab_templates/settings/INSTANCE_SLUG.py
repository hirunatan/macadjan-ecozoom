# -*- coding: utf-8 -*-

import os
from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'macadjan_%(instance_slug)s',    # Or path to database file if using sqlite3.
        'USER': '%(db_user)s',                   # Not used with sqlite3.
        'PASSWORD': '%(db_passwd)s',             # Not used with sqlite3.
        'HOST': '%(db_host)s',                   # Set to empty string for default. Not used with sqlite3.
        'PORT': '',                              # Set to empty string for default. Not used with sqlite3.
    },
    # Uncomment and fill in if you want to sync this map with other ones
    #'other': {
    #    'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    #    'NAME': 'macadjan_other',               # Or path to database file if using sqlite3.
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
    ('%(admin_name)s', '%(admin_email)s'),
)

# People that get broken-link notification emails if SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = "%(admin_email)s"
SERVER_EMAIL = '%(admin_email)s'

TIME_ZONE = '%(default_timezone)s'
LANGUAGE_CODE = '%(default_language_code)s'
LANGUAGES = (
    ('%(default_language_code)s', '%(default_language_name)s'),
)

# Skin for demo site
TEMPLATE_DIRS += (
    os.path.join(PROJECT_ROOT, 'skins/%(instance_slug)s/templates'),
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'skins/%(instance_slug)s/static'),
)

# Default marker image (used for categories or subcategories that not define their own marker).
DEFAULT_MARKER_URL = 'img/markers/icons-noun-project/otros.png'

# Entity importers for this map
MACADJAN_ENTITY_IMPORTER_PAGES = [
    ('default_csv', 'macadjan_importer.import_page_default.ImportPageDefault'),
]

# Whoosh index directory
HAYSTACK_CONNECTIONS['default']['PATH'] = os.path.join(PROJECT_ROOT, 'whoosh/index_%(instance_slug)s')

