# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('',
    url(r'^entities-text/$', EcozoomEntitiesText.as_view(), name='entities-text'),
    url(r'^entities-list/$', EcozoomEntitiesList.as_view(), name='entities-list'),
    url(r'^entities-kml/$', EcozoomEntitiesKml.as_view(), name='entities-kml'),
    url(r'^entities-georss/$', EcozoomEntitiesGeoRSS.as_view(), name='entities-georss'),
    url(r'^entity/(?P<entity_slug>[a-zA-Z0-9_\-]+)/$', EcozoomEntity.as_view(), name='entity'),
)

