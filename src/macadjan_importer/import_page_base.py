# -*- coding: utf-8 -*-

'''
Module with utilities to make web pages that allow users to execute data importers.
'''

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured

def registered_importers():
    '''
    Return all importers defined in settings.
    The returned value is a tuple (importer_name, importer_instance).
    '''
    importers_list = []
    importers_setting = getattr(settings, 'MACADJAN_ENTITY_IMPORTER_PAGES', None)
    if importers_setting:
        for (importer_name, importer_path) in importers_setting:
            importer = _load_importer(importer_path)
            importers_list.append((importer_name, importer))
    return importers_list

def find_importer(importer_name):
    filtered_importers = filter(lambda i: i[0] == importer_name, registered_importers())
    if filtered_importers:
        return filtered_importers[0][1]
    else:
        return None

def _load_importer(importer_path):
    module, attr = importer_path.rsplit('.', 1)
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured(_(u'Error importando módulo %(module)s: "%(error_msg)s")') %
                                   {'module': module, 'error_msg': unicode(e)})
    try:
        Importer = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(_(u'El módulo "%(module)s" no contiene una clase "%(class_name)s".') %
                                   {'module': module, 'class_name': attr})
    if not issubclass(Importer, ImportPage):
        raise ImproperlyConfigured(_(u'La clase "%(class_name)s" no es una subclase de "ImporPage"') %
                                   {'class_name': unicode(Importer)})
    return Importer()


class ImportPage:
    '''
    An object with all the information to ask the user the data necessary to create
    an EntityArchive and to load it with an EntityImporter. To use it, you must derive
    a new class and associate it with derived EntityArchive and EntityImporters.
    '''
    def title(self):
        '''
        Return a short string with the name of this importer.
        '''
        raise NotImplementedError()

    def intro_text(self):
        '''
        Return an optional html text to display at the top of the import page.
        '''
        return u''

    def make_form(self, request):
        '''
        Return a form prepared to ask the user all the necessary data. The form
        will be unbound or bound depending on the request method (get or post).
        '''
        raise NotImplementedError()

    def process_form(self, request, form):
        '''
        Given a bound form that has already been validated, process it and
        return a EntityArchive and a EntityConverter.
        '''
        raise NotImplementedError()

    def dispose_archive(self, request, archive):
        '''
        Get rid of the archive once finished, doing any needed cleanup.
        '''
        pass

