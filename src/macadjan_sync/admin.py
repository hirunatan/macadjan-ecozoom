#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class EntityTypeMatchInline(admin.TabularInline):
    model = EntityTypeMatch

class SubCategoryMatchInline(admin.TabularInline):
    model = SubCategoryMatch

class DBLinkAdmin(admin.ModelAdmin):
    inlines = [EntityTypeMatchInline, SubCategoryMatchInline,]

admin.site.register(DBLink, DBLinkAdmin)

class DBLinkSyncAdmin(admin.ModelAdmin):
    readonly_fields = ('finished_date', 'entities_synced',)

admin.site.register(DBLinkSync, DBLinkSyncAdmin)

