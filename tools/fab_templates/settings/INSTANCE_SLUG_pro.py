# -*- coding: utf-8 -*-

from .%(instance_slug)s import *

for database in DATABASES.values():
    database['USER'] = '%(db_user_pro)s'
    database['PASSWORD'] = '%(db_passwd_pro)s'
    database['HOST'] = '%(db_host_pro)s'
    database['PORT'] = ''

USE_ETAGS = True
DEBUG = False
PREPEND_WWW = False
TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES.append('django.middleware.gzip.GZipMiddleware')
MIDDLEWARE_CLASSES.append('django.middleware.http.ConditionalGetMiddleware')

MEDIA_ROOT = '/home/hirunatan/sites/www/%(instance_domain)s/media'
STATIC_ROOT = '/home/hirunatan/sites/www/%(instance_domain)s/static'

ROSETTA_UWSGI_AUTO_RELOAD = True

EMAIL_USE_TLS = %(email_use_tls)s
EMAIL_HOST = '%(email_host)s'
EMAIL_HOST_USER = '%(email_user)s'
EMAIL_HOST_PASSWORD = '%(email_pwd)s'
EMAIL_PORT = %(email_port)d
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

PIWIK_HOST = 'piwik.mapunto.net'
PIWIK_SITE_ID = %(piwik_site_id)s

