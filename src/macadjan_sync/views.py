# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import RedirectView, TemplateView
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.conf import settings

from macadjan import models
from macadjan_ecozoom import models as models_ecozoom
from macadjan_sync import models as models_sync
from macadjan_sync import forms

from macadjan_sync.decorators import staff_required

import types
from datetime import datetime


class SyncDBSelectView(TemplateView):
    '''
    Opening view: select a remote database to sync with.
    '''
    template_name = 'macadjan_sync/sync_db_select.html'

    def get_context_data(self, **kwargs):
        context = super(SyncDBSelectView, self).get_context_data(**kwargs)
        db_links = models_sync.DBLink.objects.all()
        context.update({
                'db_links': db_links,
            })
        return context

    @staff_required()
    def dispatch(self, *args, **kwargs):
        return super(SyncDBSelectView, self).dispatch(*args, **kwargs)


class SyncDBView(TemplateView):
    '''
    Main view: do the synchronization and show the result and the possible commands.
    '''
    template_name = 'macadjan_sync/sync_db.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SyncDBView, self).get_context_data(**kwargs)
        (grouped_list, synced_entities, discarded_entities) = self.db_link.sync_entity_lists()
        context.update({
                'db_link': self.db_link,
                'grouped_list': grouped_list,
                'synced_entities': synced_entities,
                'discarded_entities': discarded_entities,
            })
        return context

    @staff_required()
    def dispatch(self, *args, **kwargs):
        id_link = kwargs.get('id_link')
        self.db_link = get_object_or_404(models_sync.DBLink, id = id_link)
        return super(SyncDBView, self).dispatch(*args, **kwargs)


class SyncDBFinishView(TemplateView):
    '''
    Finish synchronization: show the summary of this session and a button to fix it and
    make permanent.
    '''
    template_name = 'macadjan_sync/sync_db_finish.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # No need to validate any form
        self.db_link.finish_sync()
        self.db_link.save()
        messages.success(request, _(u'Se ha completado la sincronización'))
        return HttpResponseRedirect(reverse('sync:sync-db', kwargs={'id_link': self.db_link.id}))

    def get_context_data(self, **kwargs):
        context = super(SyncDBFinishView, self).get_context_data(**kwargs)
        (grouped_list, synced_entities, discarded_entities) = self.db_link.sync_entity_lists()
        context.update({
                'db_link': self.db_link,
                'grouped_list': grouped_list,
                'synced_entities': synced_entities,
                'discarded_entities': discarded_entities,
            })
        return context

    @staff_required()
    def dispatch(self, *args, **kwargs):
        id_link = kwargs.get('id_link')
        self.db_link = get_object_or_404(models_sync.DBLink, id = id_link)
        return super(SyncDBFinishView, self).dispatch(*args, **kwargs)


class SyncDBNewView(TemplateView):
    '''
    Show an entity which is in the other database but not in the local one. Show the matching categories
    and entity type, and allow to select if multiple choices. POST to create the entity in the local
    database.
    '''
    template_name = 'macadjan_sync/sync_db_new.html'

    def get(self, request, *args, **kwargs):
        (entity_type_form, subcategory_formset) = self.get_forms()
        context = self.get_context_data(entity_type_form, subcategory_formset, None)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        (entity_type_form, subcategory_formset) = self.get_forms()

        msg_error = u''
        if entity_type_form.is_valid() and subcategory_formset.is_valid():
            # Valid forms: get the selected type and categories
            new_entity_type_id = entity_type_form.cleaned_data['entity_type_id']
            new_entity_type = get_object_or_404(models.EntityType, id = new_entity_type_id)

            new_main_subcategory = None
            new_subcategories = []
            for i, form in enumerate(subcategory_formset.forms):
                new_subcategory_slug = form.cleaned_data.get('subcategory_slug', None)
                if new_subcategory_slug:
                    new_subcategory = get_object_or_404(models.SubCategory, slug = new_subcategory_slug)
                    new_subcategories.append(new_subcategory)
                    if self.entity.main_subcategory == self.entity.subcategories.all()[i]:
                        new_main_subcategory = new_subcategory

            if not new_main_subcategory and new_subcategories:
                new_main_subcategory = new_subcategories[0]

            if new_main_subcategory:
                # Everything ok: create the entity in the local database and redirect to main sync screen
                self.db_link.create_local_entity(self.entity, new_entity_type, new_main_subcategory, new_subcategories)
                self.db_link.mark_synced_entity(self.entity)
                messages.success(request, _(u'Se ha añadido con éxito la entidad %(entidad)s') % {'entidad': self.entity.name})
                return HttpResponseRedirect(reverse('sync:sync-db', kwargs={'id_link': self.db_link.id}))
            else:
                msg_error = _(u'No se puede crear la entidad, necesita tener al menos una categoría')
        else:
            msg_error = _(u'Check the errors in the fields')

        context = self.get_context_data(entity_type_form, subcategory_formset, msg_error)
        return self.render_to_response(context)

    def get_forms(self):
        if self.request.method == 'POST':
            form_kwargs = {'data': self.request.POST}
        else:
            form_kwargs = {}

        entity_type_form = forms.EntityTypeChoiceForm(**form_kwargs)
        entity_type_form.fields['entity_type_id'].choices = [(entity_type.id, unicode(entity_type))
                                                             for entity_type in self.matching_entity_types]

        SubcategoryFormset = formset_factory(forms.SubcategoryChoiceForm, extra = len(self.other_subcategories))
        subcategory_formset = SubcategoryFormset(**form_kwargs)
        for (match, form) in zip(self.matching_subcategories, subcategory_formset.forms):
            form.fields['subcategory_slug'].choices = [(subcat.slug, unicode(subcat)) for subcat in match]

        return (entity_type_form, subcategory_formset)

    def get_context_data(self, entity_type_form, subcategory_formset, msg_error, **kwargs):
        context = super(SyncDBNewView, self).get_context_data(**kwargs)

        subcategory_pack = zip(self.other_subcategories, self.matching_subcategories, subcategory_formset.forms)

        context.update({
            'db_link': self.db_link,
            'entity': self.entity,
            'other_entity_type': self.other_entity_type,
            'entity_type_form': entity_type_form,
            'matching_entity_types': self.matching_entity_types,
            'subcategory_formset': subcategory_formset,
            'subcategory_pack': subcategory_pack,
            'msg_error': msg_error,
        })
        return context

    @staff_required()
    def dispatch(self, *args, **kwargs):
        id_link = kwargs.get('id_link')
        id_entity = kwargs.get('id_entity')

        # Get the link (local) and the entity (in the other model)
        self.db_link = get_object_or_404(models_sync.DBLink, id = id_link)
        try:
            self.entity = models_ecozoom.EcozoomEntity.objects.using(self.db_link.other_db_name).get(id = id_entity)
        except models_ecozoom.EcozoomEntity.DoesNotExist:
            raise Http404(_(u'No Entity matches the given query in %(db_name)s database') %
                            {'db_name': self.db_link.other_db_name})

        # Match type and categories
        (self.other_entity_type, self.matching_entity_types) = self.db_link.get_matching_entity_types(self.entity)
        (self.other_subcategories, self.matching_subcategories) = self.db_link.get_matching_subcategories(self.entity)

        return super(SyncDBNewView, self).dispatch(*args, **kwargs)


class SyncDBUpdateView(TemplateView):
    '''
    Show an entity which is both databases. Show all fields and allow to update any of them. POST to
    update the entity in the local database.
    '''
    template_name = 'macadjan_sync/sync_db_update.html'

    def get(self, request, *args, **kwargs):
        entity_update_form = self.get_form()
        context = self.get_context_data(entity_update_form, None)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        entity_update_form = self.get_form()

        msg_error = u''
        if entity_update_form.is_valid():

            # Everything ok: update the entity in the local database and redirect to main sync screen
            updated_entity = entity_update_form.save()
            # Set the dates manually, to avoid automatic setting of modification_date
            updated_entity.modification_date = entity_update_form.cleaned_data['modification_date']
            updated_entity.save(update_dates = False)
            self.db_link.mark_synced_entity(self.entity_local)
            messages.success(request, _(u'Se ha actualizado con éxito la entidad %(entidad)s') % {'entidad': self.entity_local.name})
            return HttpResponseRedirect(reverse('sync:sync-db', kwargs={'id_link': self.db_link.id}))

        else:
            msg_error = _(u'Check the errors in the fields')

        context = self.get_context_data(entity_update_form, msg_error)
        return self.render_to_response(context)

    def get_form(self):
        if self.request.method == 'POST':
            form_kwargs = {'data': self.request.POST}
        else:
            form_kwargs = {}

        entity_update_form = forms.EntityUpdateForm(instance = self.entity_local, **form_kwargs)

        return entity_update_form

    def get_context_data(self, entity_update_form, msg_error, **kwargs):
        context = super(SyncDBUpdateView, self).get_context_data(**kwargs)

        # Pack the list of fields of the form, together with the values of both entities formatted for
        # the javascript functions and for displaying in html.
        packed_fields = []
        for field in entity_update_form:

            local_value = getattr(self.entity_local, field.name)
            if local_value == None or local_value == u'':
                reset_value = u''
            elif type(local_value) == types.BooleanType:
                reset_value = None
	    elif isinstance(local_value, datetime):
                reset_value = local_value.strftime('%d/%m/%Y %H:%M')
            elif hasattr(local_value, 'all'):
                reset_value = None
            elif field.name == 'entity_type' or field.name == 'main_subcategory':
                reset_value = None
            else:
                reset_value = unicode(local_value).replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\\n').replace("'", "\\'")

            other_value = getattr(self.entity_other, field.name)
            if other_value == None or other_value == u'':
                display_value = u''
                update_value = None
            elif type(other_value) == types.BooleanType:
                display_value = _(u'Sí') if other_value else _(u'No')
                update_value = None
	    elif isinstance(other_value, datetime):
                display_value = other_value.strftime('%d/%m/%Y %H:%M')
                update_value = other_value.strftime('%d/%m/%Y %H:%M')
            elif hasattr(other_value, 'all'):
                display_value = '<br />'.join([unicode(value) for value in other_value.all()])
                update_value = None
            elif field.name == 'entity_type' or field.name == 'main_subcategory':
                display_value = unicode(other_value)
                update_value = None
            else:
                display_value = unicode(other_value).replace('\r\n', '\n').replace('\r', '\n').replace('\n', '<br />')
                update_value = unicode(other_value).replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\\n').replace("'", "\\'")

            packed_fields.append([field, reset_value, display_value, update_value])

        context.update({
            'db_link': self.db_link,
            'entity_other': self.entity_other,
            'entity_local': self.entity_local,
            'entity_update_form': entity_update_form,
            'packed_fields': packed_fields,
            'msg_error': msg_error,
        })

        return context

    @staff_required()
    def dispatch(self, *args, **kwargs):
        id_link = kwargs.get('id_link')
        id_entity_other = kwargs.get('id_entity_other')
        id_entity_local = kwargs.get('id_entity_local')

        # Get the link (local) and the entity (in both other and local models)
        self.db_link = get_object_or_404(models_sync.DBLink, id = id_link)
        try:
            self.entity_other = models_ecozoom.EcozoomEntity.objects.using(self.db_link.other_db_name).get(id = id_entity_other)
        except models_ecozoom.EcozoomEntity.DoesNotExist:
            raise Http404(_(u'No Entity matches the given query in %(db_name)s database') %
                            {'db_name': self.db_link.other_db_name})
        try:
            self.entity_local = models_ecozoom.EcozoomEntity.objects.get(id = id_entity_local)
        except models_ecozoom.EcozoomEntity.DoesNotExist:
            raise Http404(_(u'No Entity matches the given query in local database'))

        return super(SyncDBUpdateView, self).dispatch(*args, **kwargs)


class SyncDBDiscardView(RedirectView):
    '''
    Get an entity which is in the other database but not in the local one, and discard it.
    '''
    def get(self, request, *args, **kwargs):
        self.db_link.mark_discarded_entity(self.entity)
        messages.success(request, _(u'Se ha descartado la entidad %(entidad)s') % {'entidad': self.entity.name})
        return super(SyncDBDiscardView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse('sync:sync-db', kwargs={'id_link': self.db_link.id})

    @staff_required()
    def dispatch(self, *args, **kwargs):
        id_link = kwargs.get('id_link')
        id_entity = kwargs.get('id_entity')

        # Get the link (local) and the entity (in the other model)
        self.db_link = get_object_or_404(models_sync.DBLink, id = id_link)
        try:
            self.entity = models_ecozoom.EcozoomEntity.objects.using(self.db_link.other_db_name).get(id = id_entity)
        except models_ecozoom.EcozoomEntity.DoesNotExist:
            raise Http404(_(u'No Entity matches the given query in %(db_name)s database') %
                            {'db_name': self.db_link.other_db_name})

        return super(SyncDBDiscardView, self).dispatch(*args, **kwargs)

