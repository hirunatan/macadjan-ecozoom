# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _

from macadjan.admin import EntityAdmin

from . import models

class EcozoomEntityAdmin(EntityAdmin):
    list_filter = ('is_active', 'subcategories', 'map_source')

admin.site.register(models.EcozoomEntity, EcozoomEntityAdmin)

