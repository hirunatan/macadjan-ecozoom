# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.conf import settings

from macadjan.models import SiteInfo

def current_site_info(request):
    '''Adds the site info for the current site to all template contexts.'''
    current_site = Site.objects.get_current()
    try:
        site_info = current_site.site_info
        return {'current_site_info': site_info}
    except SiteInfo.DoesNotExist:
        return {'current_site_info': None}


def is_sync_installed(request):
    '''Checks if macadjan_sync application is installed.'''
    is_sync = 'macadjan_sync' in settings.INSTALLED_APPS
    return {'IS_SYNC_INSTALLED': is_sync}


def piwik_settings(request):
    '''Adds piwik settings to all template contexts.'''
    host = getattr(settings, 'PIWIK_HOST', None)
    if host == None:
        raise ValueError(u'You need to define PIWIK_HOST in your django settings file.')
    site_id = getattr(settings, 'PIWIK_SITE_ID', None)
    if site_id == None:
        raise ValueError(u'You need to define PIWIK_SITE_ID in your django settings file.')
    return {'PIWIK_HOST': host, 'PIWIK_SITE_ID': site_id}

