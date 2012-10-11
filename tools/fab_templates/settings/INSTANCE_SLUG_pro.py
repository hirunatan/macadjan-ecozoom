# -*- coding: utf-8 -*-

from .%(instance_slug)s import *

for database in DATABASES.values():
    database['USER'] = '$(db_user_pro)s'
    database['PASSWORD'] = '$(db_passwd_pro)s'
    database['HOST'] = '$(db_host_pro)'
    database['PORT'] = ''

USE_ETAGS = True
DEBUG = False
PREPEND_WWW = False
TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES.append('django.middleware.gzip.GZipMiddleware')
MIDDLEWARE_CLASSES.append('django.middleware.http.ConditionalGetMiddleware')

MEDIA_ROOT = '/home/hirunatan/sites/www/$(instance_domain)s/media'
STATIC_ROOT = '/home/hirunatan/sites/www/$(instance_domain)s/static'

ROSETTA_UWSGI_AUTO_RELOAD = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mapa.arkipelagos@gmail.com'
EMAIL_HOST_PASSWORD = 'coigaarkipelagos'
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

PIWIK_HOST = 'piwik.mapunto.net'
PIWIK_SITE_ID = %(piwik_site_id)s

