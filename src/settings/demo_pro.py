# -*- coding: utf-8 -*-

# Change demo for your site name
from .demo import *

USE_ETAGS = True
DEBUG = False
PREPEND_WWW = False
TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES.append('django.middleware.gzip.GZipMiddleware')
MIDDLEWARE_CLASSES.append('django.middleware.http.ConditionalGetMiddleware')

