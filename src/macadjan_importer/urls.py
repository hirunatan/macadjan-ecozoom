# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

from .views import *

urlpatterns = patterns('',
    # Admin screens to load entities from a file or an external source.
    url(r'^$', ImportSelect.as_view(), name='import-select'),
    url(r'^(?P<importer_name>[a-zA-Z0-9_\-]+)/$', Import.as_view(), name='import'),
    url(r'^(?P<importer_name>[a-zA-Z0-9_\-]+)/finish/$', ImportFinish.as_view(), name='import-finish'),
)

