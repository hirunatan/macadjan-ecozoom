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

    def get_form(self, request, obj=None, **kwargs):
        form = super(EntityProposalAdmin, self).get_form(request, obj, **kwargs)
        if obj and obj.existing_entity:
            for field_name,field in form.base_fields.items():
                original_value = getattr(obj.existing_entity, field_name, None)
                if original_value!=None and original_value!=getattr(obj, field_name, None):
                    field.help_text += '<br><div style="color:#FF0000"> '
                    if field_name == 'subcategories':
                        subcategories_changed = False
                        actual_subcategories = getattr(obj,'subcategories',None).all()
                        if actual_subcategories:
                            for sub in actual_subcategories:
                                if not sub in original_value.all():
                                    subcategories_changed = True
                        elif original_value.all():
                            subcategories_changed = True 
                        if subcategories_changed:
                            field.help_text += '<br><b>Valor original:</b> '
                            for category in original_value.all():
                                field.help_text += unicode(category) + '<br>'
                    else:
                        field.help_text += '<b>Valor original:</b> ' + unicode(original_value)
                    field.help_text += '</div>'
        return form

admin.site.register(models.EntityProposal, EntityProposalAdmin)

