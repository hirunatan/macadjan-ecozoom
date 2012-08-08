# -*- coding: utf-8 -*-

from django import forms
from django.forms import formsets
from django.forms.widgets import DateTimeInput
from macadjan_ecozoom import models as models_ecozoom

class EntityTypeChoiceForm(forms.Form):
    '''
    Form to choose an entity type.
    '''
    entity_type_id = forms.ChoiceField(choices = [], required = True)

class SubcategoryChoiceForm(forms.Form):
    '''
    Form to choose a subcategory.
    '''
    subcategory_slug = forms.ChoiceField(choices = [], required = True)

class EntityUpdateForm(forms.ModelForm):
    '''
    Form to edit an entity by updating it from another one in the other database.
    '''
    class Meta:
        model = models_ecozoom.EcozoomEntity
        exclude = ('slug', 'is_container', 'contained_in', 1)

    def __init__(self, *args, **kwargs):
	super(EntityUpdateForm, self).__init__(*args, **kwargs)
	self.fields['creation_date'].widget = DateTimeInput(format='%d/%m/%Y %H:%M')
	self.fields['modification_date'].widget = DateTimeInput(format='%d/%m/%Y %H:%M')

