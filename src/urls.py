# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('macadjan_ecozoom.urls')),
    url(r'^', include('macadjan.urls')),
    url(r'^sync_db/', include('macadjan_sync.urls')),
    url(r'^entity_proposal/', include('macadjan_form.urls')),
    url(r'^import/', include('macadjan_importer.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^captcha/', include('captcha.urls')),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

