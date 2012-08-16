#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _

from . import models

class EntityProposalAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'alias', 'main_subcategory', 'creation_date', 'modification_date', 'status') # Fields shown in the entity list
    filter_vertical = ('subcategories',)   # Fields that use a selection widget instead a multi select
    list_filter = ('status', 'subcategories',)         # Fields you can filter by in the entity list
    search_fields = ('name', 'alias',)       # Fields searched by the input bux in the entity list

admin.site.register(models.EntityProposal, EntityProposalAdmin)

