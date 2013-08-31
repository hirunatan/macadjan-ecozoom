# -*- coding: utf-8 -*-

'''
Module with utilities to import entities into Macadjan database, from an external source.
'''

from django.utils.translation import ugettext as _
from macadjan_ecozoom import models
#from macadjan_base.async_tasks import task__geolocalize_entity

class EntityImporter:
    '''
    An object that can import entities from an archive and a converter.
    '''
    def __init__(self, archive, converter):
        self.archive = archive
        self.converter = converter
        self.errors = None
        self.imported_items = None

    def import_entities(self):
        '''
        Import all entities in an archive into Macadjan database, using the converter to
        convert the format. The entities that are already in the database (identified by
        the slug) will be updated; others will be created. No entity will be deleted.

        If everything was ok, self.has_errors() will be False. If any problem ocurred, in
        self.errors there will be a list of one or more error messages.
        '''
        self.errors = []
        self.imported_items = []
        try:
            self.converter.initialize(self.archive)
        except Exception as ex:
            self.process_exception(_(u'Error general'), ex)
        else:
            for item in self.archive:
                try:
                    self.process_item(item)
                except Exception as ex:
                    self.process_exception(_(u'Error en posición %(position)d') %
                            {'position': self.archive.current_pos()}, ex)
        finally:
            try:
                self.converter.finish(self.archive)
            except Exception as ex:
                self.process_exception(_(u'Error cerrando el archivo'), ex)

    def process_item(self, item):
        slug = self.converter.get_slug_from_item(item)
        try:
            entity = models.EcozoomEntity.objects.get(slug = slug)
            if entity.map_source != self.converter.map_source:
                raise ValueError(_(u'No se ha podido cargar "%(name)s" porque pertenece a otra fuente de mapeo: %(map_source)s') %
                        {'name': entity.name, 'map_source': entity.map_source})
        except models.EcozoomEntity.DoesNotExist:
            entity = models.EcozoomEntity()
        (entity, m2m) = self.converter.load_entity_from_item(entity, item)
        entity.save(update_dates = False)
        #if not entity.latitude or not entity.longitude:
        #    task__geolocalize_entity.delay(entity.pk)
        for subcategory in m2m['subcategories']:
            entity.subcategories.add(subcategory)
        for tag in m2m['tags']:
            entity.tags.add(tag)
        self.imported_items.append(entity)

    def process_exception(self, intro_message, exception):
        self.errors.append('%s: (%s) %s' % (intro_message,
                                            exception.__class__.__name__,
                                            unicode(exception)))

    def has_errors(self):
        if self.errors == None:
            raise ValueError(_(u'No se pueden consultar los errores antes de importar.'))
        else:
            return (len(self.errors) > 0)

    def imported_items(self):
        return self.imported_items


class EntityConverter:
    '''
    An object with all the information to convert an item coming from a specific
    EntityArchive into a macadjan Entity. To use it, you must derive a new class
    and associate it with a derived EntityArchive.
    '''
    def __init__(self, map_source):
        self.map_source = map_source

    def initialize(self, archive):
        '''
        Given an archive, do whatever it's needed before start reading items.
        '''
        pass

    def finish(self, archive):
        '''
        Given an archive, do whatever it's needed after all items have been read.
        '''
        pass

    def get_slug_from_item(self, item):
        '''
        Given an archive item, return the slug, to check if it exists or not
        in Macadjan database.
        '''
        raise NotImplementedError()

    def load_entity_from_item(self, entity, item):
        '''
        Given an archive item, copy all the available fields to the entity.

        Then, return the modified entity and a list with the many-to-many relations
        that must be filled in (currently only subcategory).

        So the return value is (entity, {'subcategories': [subcategory1, subcategory2,...]})
        '''
        raise NotImplementedError()

