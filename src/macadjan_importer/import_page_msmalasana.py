# -*- coding: utf-8 -*-

import os, tempfile

from django import forms
from django.utils.translation import ugettext as _

from macadjan.models import MapSource, MacadjanUserProfile
from .import_page_base import ImportPage
from .archive_csv import EntityArchiveCSV
from .converter_msmalasana import EntityConverterMSMalasana


class ImportPageMSMalasana(ImportPage):
    '''
    Subclass of ImportPage that use EntityArchiveCSV and ConverterMSMalasana to submit
    a csv file exported from MS Malasaña spreadsheet and load into the database.
    '''
    def title(self):
        '''
        Return a short string with the name of this importer.
        '''
        return _(u'Importar desde un fichero csv del Mercado Social Malasaña')

    def intro_text(self):
        '''
        Return a html text to display at the top of the import page.
        '''
        # Translator: don't remove or change the <p> and </p> markers.
        return _(u'<p>Necesitas un fichero csv generado a partir de la hoja de cálculo oficial del MS Malasaña.</p>')

    def make_form(self, request):
        '''
        Return a form prepared to ask the user all the necessary data. The form
        will be unbound or bound depending on the request method (get or post).
        '''
        if request.method == 'GET':
            form = UploadCSVForm()
        else:
            form = UploadCSVForm(request.POST, request.FILES)

        user = request.user
        profile = MacadjanUserProfile.objects.get_for_user(user)
        if profile and profile.map_source:
            form.fields['map_source'].initial = profile.map_source
            if not user.is_superuser:
                form.fields['map_source'].widget = forms.HiddenInput()

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
        converter = EntityConverterMSMalasana(map_source)
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

