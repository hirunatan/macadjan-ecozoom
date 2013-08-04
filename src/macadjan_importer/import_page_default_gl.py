# -*- coding: utf-8 -*-

import os, tempfile

from django import forms
from django.utils.translation import ugettext as _

from macadjan.models import MapSource
from .import_page_base import ImportPage
from .archive_csv import EntityArchiveCSV
from .converter_default_gl import EntityConverterDefault


class ImportPageDefault(ImportPage):
    '''
    Subclass of ImportPage that use EntityArchiveCSV and ConverterDefault to submit
    a spreadsheet with the default Macadjan format and load into the database.
    '''
    def title(self):
        '''
        Return a short string with the name of this importer.
        '''
        return _(u'Importar desde un fichero csv (galego)')

    def intro_text(self):
        '''
        Return a html text to display at the top of the import page.
        '''
        # Translator: don't remove or change the <p> and </p> markers.
        return _(u'<p>Necesitas un fichero creado a partir de la hoja de cálculo de carga de ficheros, y guardada en formato csv.</p>')

    def make_form(self, request):
        '''
        Return a form prepared to ask the user all the necessary data. The form
        will be unbound or bound depending on the request method (get or post).
        '''
        if request.method == 'GET':
            form = UploadCSVForm()
        else:
            form = UploadCSVForm(request.POST, request.FILES)
        return form

    def process_form(self, request, form):
        '''
        Given a bound form that has already been validated, process it and
        return a EntityArchive and a EntityConverter.
        '''
        map_source = form.cleaned_data['map_source']
        uploaded_file = request.FILES['csv_file']
        temp_file = tempfile.NamedTemporaryFile(delete = False)
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        temp_file.close()
        archive = EntityArchiveCSV(temp_file.name)
        converter = EntityConverterDefault(map_source)
        return (archive, converter)

    def dispose_archive(self, request, archive):
        '''
        Get rid of the archive once finished, doing any needed cleanup.
        '''
        os.unlink(archive.filename)


class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(required = True, label = _(u'Selecciona un fichero csv'))
    map_source = forms.ModelChoiceField(queryset = MapSource.objects.all(),
                      required = True, label = _(u'Indica la fuente de datos'))

