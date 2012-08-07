# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.views.generic import TemplateView

from macadjan_sync.decorators import staff_required

from . import import_page_base, converter_base


class ImportSelect(TemplateView):
    '''
    Opening view of imports: select a importer to work with.
    '''
    template_name = 'macadjan_importer/import_select.html'

    def get_context_data(self, **kwargs):
        context = super(ImportSelect, self).get_context_data(**kwargs)
        importers = import_page_base.registered_importers
        context.update({
                'importers': importers,
            })
        return context

    @staff_required()
    def dispatch(self, request, *args, **kwargs):
        return super(ImportSelect, self).dispatch(request, *args, **kwargs)


class Import(TemplateView):
    '''
    Main import view: show the importer form and process it.
    '''
    template_name = 'macadjan_importer/import_form.html'

    def get(self, request, *args, **kwargs):
        self.import_form = self.importer.make_form(request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.import_form = self.importer.make_form(request)
        if self.import_form.is_valid():
            archive, converter = self.importer.process_form(request, self.import_form)
            entity_importer = converter_base.EntityImporter(archive, converter)
            entity_importer.import_entities()
            self.importer.dispose_archive(request, archive)
            if entity_importer.has_errors():
                messages.error(request, _(u'Ha habido errores en la importación'))
            else:
                messages.success(request, _(u'Se ha completado la importación sin errores'))
            request.session['import_errors'] = entity_importer.errors
            request.session['import_result'] = entity_importer.imported_items
            return HttpResponseRedirect(reverse('import-finish', kwargs={'importer_name': self.importer_name}))
        else:
            messages.error(request, _(u'No se han podido importar los datos'))
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(Import, self).get_context_data(**kwargs)
        context.update({
                'importer_name': self.importer_name,
                'importer': self.importer,
                'intro_text': self.importer.intro_text(),
                'import_form': self.import_form,
            })
        return context

    @staff_required()
    def dispatch(self, request, *args, **kwargs):
        self.importer_name = kwargs.get('importer_name')
        self.importer = import_page_base.find_importer(self.importer_name)
        if not self.importer:
            raise Http404()
        return super(Import, self).dispatch(request, *args, **kwargs)


class ImportFinish(TemplateView):
    '''
    Show the final result of an import.
    '''
    template_name = 'macadjan_importer/import_finish.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ImportFinish, self).get_context_data(**kwargs)
        context.update({
                'importer_name': self.importer_name,
                'importer': self.importer,
                'import_errors': self.import_errors,
                'import_result': self.import_result,
            })
        return context

    @staff_required()
    def dispatch(self, request, *args, **kwargs):
        self.importer_name = kwargs.get('importer_name')
        self.importer = import_page_base.find_importer(self.importer_name)
        if not self.importer:
            raise Http404()
        self.import_errors = request.session['import_errors']
        self.import_result = request.session['import_result']
        return super(ImportFinish, self).dispatch(request, *args, **kwargs)

