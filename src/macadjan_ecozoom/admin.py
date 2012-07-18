# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _

from macadjan.admin import EntityAdmin

from . import models

admin.site.register(models.MapSource)
admin.site.register(models.EcozoomEntity, EntityAdmin)

