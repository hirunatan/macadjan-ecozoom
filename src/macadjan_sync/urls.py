# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

from macadjan_sync.views import *

urlpatterns = patterns('',
    url(r'^new/(?P<id_link>\d+)/(?P<id_entity>\d+)/$',
            SyncDBNewView.as_view(), name='sync-db-new'),
    url(r'^update/(?P<id_link>\d+)/(?P<id_entity_other>\d+)/(?P<id_entity_local>\d+)$',
            SyncDBUpdateView.as_view(), name='sync-db-update'),
    url(r'^finish/(?P<id_link>\d+)/$',
            SyncDBFinishView.as_view(), name='sync-db-finish'),
    url(r'^discard/(?P<id_link>\d+)/(?P<id_entity>\d+)$',
            SyncDBDiscardView.as_view(), name='sync-db-discard'),
    url(r'^(?P<id_link>\d+)/$',
            SyncDBView.as_view(), name='sync-db'),
    url(r'^$',
            SyncDBSelectView.as_view(), name='sync-db-select'),
)

