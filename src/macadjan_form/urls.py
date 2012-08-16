# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

from .views import *

urlpatterns = patterns('',
    url(r'^new/$', EntityProposal.as_view(), name='entity-proposal'),
    url(r'^change/(?P<entity_slug>[a-zA-Z0-9_\-]+)/$', EntityProposal.as_view(), name='entity-proposal'),
    url(r'^ok/$', EntityProposalOk.as_view(), name='entity-proposal-ok'),
    url(r'^ok/(?P<entity_slug>[a-zA-Z0-9_\-]+)/$', EntityProposalOk.as_view(), name='entity-proposal-ok'),
)

