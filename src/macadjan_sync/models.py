# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from macadjan import models as models_macadjan
from macadjan_ecozoom import models as models_ecozoom

import logging
traces = logging.getLogger('traces')

class EntityTypeMatch(models.Model):
    db_link = models.ForeignKey('DBLink', null = False, blank = False,
            related_name = 'entity_type_matches',
            verbose_name = _(u'Conexión BD'),
            help_text = _(u'A qué conexión BD pertenece este enlace'))

    local_entity_type = models.ForeignKey(models_macadjan.EntityType, null = False, blank = False,
            related_name = 'entity_type_matches',
            verbose_name = _(u'Tipo de entidad local'),
            help_text = _(u'Tipo de entidad en la BD local'))

    other_entity_type_id = models.IntegerField(null = False, blank = False,
            verbose_name = _(u'Tipo de entidad otra BD'),
            help_text = _(u'Id del tipo de entidad de la otra BD'))

    def __unicode__(self):
        return _(u'Sincr tipo de entidad %(local_cat)s <- %(other_cat)s') % \
                 {'local_cat': self.local_entity_type.id,
                  'other_cat': self.other_entity_type_id}

    class Meta:
        ordering = ['other_entity_type_id']
        verbose_name = _(u'vínculo tipo de entidad')
        verbose_name_plural = _(u'vínculos tipos de entidad')


class SubCategoryMatch(models.Model):
    db_link = models.ForeignKey('DBLink', null = False, blank = False,
            related_name = 'subcategory_matches',
            verbose_name = _(u'Conexión BD'),
            help_text = _(u'A qué conexión BD pertenece este enlace'))

    local_subcategory = models.ForeignKey(models_macadjan.SubCategory, null = False, blank = False,
            related_name = 'subcategory_matches',
            verbose_name = _(u'Categoría local'),
            help_text = _(u'Categoría en la BD local'))

    other_subcategory_slug = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Categoría otra BD'),
            help_text = _(u'Slug de la subcategoría de la otra BD'))

    def __unicode__(self):
        return _(u'Sincr subcategoría %(local_cat)s <- %(other_cat)s') % \
                 {'local_cat': self.local_subcategory.slug,
                  'other_cat': self.other_subcategory_slug}

    class Meta:
        ordering = ['local_subcategory__category__name', 'other_subcategory_slug']
        verbose_name = _(u'vínculo subcategoría')
        verbose_name_plural = _(u'vínculos subcategorías')


class DBLink(models.Model):
    other_db_name = models.CharField(max_length = 100, null = False, blank = False,
            verbose_name = _(u'Otra BD'),
            help_text = _(u'Nombre de la otra base de datos'))
    map_source = models.ForeignKey('macadjan.MapSource', related_name = 'db_links', null = False, blank = False,
            verbose_name = _(u'Fuente'),
            help_text = _('Fuente de mapeo vinculada a esta base de datos'))

    def __unicode__(self):
        return _(u'Sincr default <-> %(other_db)s') % {'other_db': self.other_db_name}

    class Meta:
	ordering = ['other_db_name']
	verbose_name = _(u'conexión otra BD')
	verbose_name_plural = _(u'conexiones otras BD')

    def save(self, *args, **kwargs):
        new_link = (not self.id)
        super(DBLink, self).save(*args, **kwargs)
        if new_link:
            self.generate_type_matches()
            self.generate_subcategory_matches()

    def generate_type_matches(self):
        '''
        Generate an initial set of type matches, assuming that types in the other db
        are the same as in the local db (only true matches are created).
        '''
        for local_entity_type in models_macadjan.EntityType.objects.order_by('name').all():
            try:

                other_entity_type = \
                    models_macadjan.EntityType.objects.using(self.other_db_name).get(name = local_entity_type.name)
                self.entity_type_matches.create(local_entity_type = local_entity_type,
                                                other_entity_type_id = other_entity_type.id)

            except models_macadjan.EntityType.DoesNotExist:
                pass

    def generate_subcategory_matches(self):
        '''
        Generate an initial set of subcategory matches, assuming that subcategories in the other db
        are the same as in the local db (only true matches are created).
        '''
        for local_subcategory in models_macadjan.SubCategory.objects.order_by('slug').all():
            try:

                other_subcategory = \
                    models_macadjan.SubCategory.objects.using(self.other_db_name).get(slug = local_subcategory.slug)
                self.subcategory_matches.create(local_subcategory = local_subcategory,
                                                other_subcategory_slug = other_subcategory.slug)

            except models_macadjan.SubCategory.DoesNotExist:
                pass


    def get_current_sync(self):
        '''
        Get the DBLinkSync with finished_date = NULL (i.e. the current sync). If it
        does not exist, create it.
        '''
        syncs = self.syncs.filter(finished_date__isnull = True)
        if not syncs:
            current_sync = DBLinkSync(db_link = self)
            current_sync.save()
        else:
            current_sync = syncs[0]
        return current_sync

    def get_last_finished_sync_datetime(self):
        '''
        Get the datetime of the latest finished DBLinkSync. If there is no finished ones,
        return datetime.min.
        '''
        syncs = self.syncs.filter(finished_date__isnull = False).order_by('-finished_date')
        if not syncs:
            return datetime.min
        else:
            return syncs[0].finished_date

    def sync_entity_lists(self):
        '''
        Get a DBLink object and two lists of entities, sorted by slug. Find all entities in the 'other' list
        that have been modified after the last sync, and classify them in four groups:
         - new_entities: the ones that do not have a matching in the 'local' list (match by slug)
         - modified_entities: the ones that have a matching one, and the other one has been modified.
         - conflict_entities: matching entities that have been modified in both lists.
         - synced_entities: entities already synced in this session (both new, modified and conflict).
         - discarded_entities: entities from the other db that have been discarded, not to sync.

        Finally, pack the three first groups, grouped by subcategory, in a list like this:
            list = [('subcategory_1', (new_entities_1, modified_entities_1, conflict_entities_1)),
                    ('subcategory_2', (new_entities_2, modified_entities_2, conflict_entities_2)),
                    ...]
        '''
        new_entities = []
        modified_entities = []
        conflict_entities = []
        synced_entities = []
        discarded_entities = []

        local_entities = models_ecozoom.EcozoomEntity.objects.order_by('slug').all()
        other_entities = models_ecozoom.EcozoomEntity.objects.using(self.other_db_name).order_by('slug').all()

        local_iter = local_entities.iterator()
        other_iter = other_entities.iterator()

        local_entity = get_next(local_iter)
        other_entity = get_next(other_iter)

        current_sync = self.get_current_sync()
        last_sync = self.get_last_finished_sync_datetime()

        discarded_ids = current_sync.discarded_ids()

        # Iterate both lists simultaneously
        while local_entity and other_entity:

	    # Uncomment to trace the sync algorythm
	    #traces.debug('%45s %45s' % (local_entity.slug[:45], other_entity.slug[:45]))
            if local_entity.slug.lower() == other_entity.slug.lower():  # mysql ignores case when sorting
                # Matching entity
                if local_entity in current_sync.entities_synced.all():
                    synced_entities.append(local_entity)
                elif other_entity.modification_date > last_sync:
                    if local_entity.modification_date > last_sync:
                        conflict_entities.append((local_entity, other_entity))
                    else:
                        modified_entities.append((local_entity, other_entity))
                local_entity = get_next(local_iter)
                other_entity = get_next(other_iter)

            elif local_entity.slug.lower() > other_entity.slug.lower():
                # New entity
                if other_entity.id in discarded_ids:
                    discarded_entities.append(other_entity)
                else:
                    if other_entity.modification_date > last_sync:
                        new_entities.append(other_entity)
                other_entity = get_next(other_iter)

                # New entity (only if it has at least one convertible subcategory) (NO, is better all of them)
                #if other_entity.modification_date > last_sync:
                    #for subcategory in other_entity.subcategories.all():
                    #    matches = SubCategoryMatch.objects.filter(other_subcategory_slug=subcategory.slug)
                    #    if matches:
                    #       new_entities.append(other_entity)
                    #        break

            else:
                # Only local entity
                if local_entity in current_sync.entities_synced.all():
                    synced_entities.append(local_entity)
                local_entity = get_next(local_iter)

        # Process remaining entities at the end of any list
        while local_entity:
            if local_entity in current_sync.entities_synced.all():
                synced_entities.append(local_entity)
            local_entity = get_next(local_iter)

        while other_entity:
            if other_entity.modification_date > last_sync:
                if other_entity.id in discarded_ids:
                    discarded_entities.append(other_entity)
                else:
                    new_entities.append(other_entity)
                #for subcategory in other_entity.subcategories.all():
                #    matches = SubCategoryMatch.objects.filter(other_subcategory_slug=subcategory.slug)
                #    if matches:
                #        new_entities.append(other_entity)
                #        break
            other_entity = get_next(other_iter)

        # Group by categories
        grouped_dict = {}

        for entity in new_entities:
            key = unicode(entity.main_subcategory)
            if key not in grouped_dict:
                grouped_dict[key] = ([], [], [])
            grouped_dict[key][0].append(entity)

        for local_entity, other_entity in modified_entities:
            key = unicode(other_entity.main_subcategory)
            if key not in grouped_dict:
                grouped_dict[key] = ([], [], [])
            grouped_dict[key][1].append((local_entity, other_entity))

        for local_entity, other_entity in conflict_entities:
            key = unicode(other_entity.main_subcategory)
            if key not in grouped_dict:
                grouped_dict[key] = ([], [], [])
            grouped_dict[key][2].append((local_entity, other_entity))

        grouped_list = grouped_dict.items()
        grouped_list.sort() # sort by the first element of the tuple; in this case, the key
        grouped_list = map(lambda x: (x[0], x[1][0], x[1][1], x[1][2]), grouped_list)

        return (grouped_list, synced_entities, discarded_entities)


    def get_matching_entity_types(self, entity):
        '''
        Get the type of an entity of the other db, and get a list with the matching types in the local one
        '''
        other_entity_type = entity.entity_type
        matches = EntityTypeMatch.objects.filter(other_entity_type_id=other_entity_type.id)
        match_types = [match.local_entity_type for match in matches.all()]

        return (other_entity_type, match_types)


    def get_matching_subcategories(self, entity):
        '''
        Take all the subcategories of an entity of the other db, and get a list with the matching
        categories in the local one.
        '''
        other_subcategories = entity.subcategories.all()
        match_subcategories = []
        for other_subcategory in other_subcategories:
            matches = SubCategoryMatch.objects.filter(other_subcategory_slug=other_subcategory.slug)
            match_subcategories.append([match.local_subcategory for match in matches.all()])

        return (other_subcategories, match_subcategories)


    def create_local_entity(self, entity, new_entity_type, new_main_subcategory, new_subcategories):
        '''
        Create a local entity equal to the given one.
        '''
        # Ensure the entity is given a new id in the local db
        entity.pk = None

        # Clear the "contained in" field (if needed, you must restore it manually later)
        entity.contained_in = None

        # Remove external references to avoid problems when changing the db
        entity.entity_type = None
        entity.main_subcategory = None
        entity.map_source = None

        # Save in the default database and add to the synced list
        entity.save(using = 'default')

        # Set the new type, categories and source
        entity.entity_type = new_entity_type
        entity.main_subcategory = new_main_subcategory
        entity.map_source = self.map_source
        entity.save()


        # Add the new subcategories
        for subcat in new_subcategories:
            entity.subcategories.add(subcat)

    def mark_synced_entity(self, entity):
        '''
        Add the entity to the entities_synced list of the current DBLinkSync.
        '''
        current_sync = self.get_current_sync()
        current_sync.entities_synced.add(entity)

    def mark_discarded_entity(self, entity):
        '''
        Add the entity (in the other database) to the discarded list of the current DBLinkSync.
        '''
        current_sync = self.get_current_sync()
        discarded = DBLinkDiscarded(db_link_sync = current_sync,
                                    other_entity_id = entity.id)
        discarded.save()

    def finish_sync(self):
        '''
        Finish the synchronization. Memorize the current date and time and close the current sync. Any entity
        not synced yet will be marked to ignore. A new sync is created, from now on only entities that are
        modified again will be available for syncing.
        '''
        current_sync = self.get_current_sync()
        current_sync.finished_date = datetime.now()
        current_sync.save()
        # Get the current sync again, so that a new one is created.
        current_sync = self.get_current_sync()


def get_next(the_list):
    try:
        obj = the_list.next()
        return obj
    except StopIteration:
        return None


class DBLinkSync(models.Model):

    db_link = models.ForeignKey('DBLink', null = False, blank = False,
            related_name = 'syncs',
            verbose_name = _(u'Conexión BD'),
            help_text = _(u'A qué conexión BD pertenece esta sincronización'))

    finished_date = models.DateTimeField(null = True, blank = True,
            verbose_name = _(u'fecha de fin de la sincronización'),
            help_text = _(u'Fecha y hora de finalización de esta sincronización'))

    entities_synced = models.ManyToManyField(models_ecozoom.EcozoomEntity, null = True, blank = True,
            related_name = 'sync_data',
            verbose_name = _(u'Entidades sincronizadas'))

    def __unicode__(self):
        return _(u'Sincr default <-> %(other_db)s [%(finished_date)s]') % {
                    'other_db': self.db_link.other_db_name,
                    'finished_date': self.finished_date.strftime('%c') if self.finished_date else _(u'Actual'),
                    }

    def discarded_ids(self):
        return self.discarded.values_list('other_entity_id', flat = True)

    def discarded_entities(self):
        return models_ecozoom.EcozoomEntity.objects.using(self.db_link.other_db_name).filter(id__in = self.discarded_ids())

    class Meta:
	ordering = ['db_link', 'finished_date']
	verbose_name = _(u'sincronización con otra BD')
	verbose_name_plural = _(u'sincronizaciones con otras BD')


class DBLinkDiscarded(models.Model):

    db_link_sync = models.ForeignKey('DBLinkSync', null = False, blank = False,
            related_name = 'discarded',
            verbose_name = _(u'sincronización'),
            help_text = _(u'A qué sincronización de una conexión BD pertenece esta sincronización'))

    other_entity_id = models.IntegerField(null = False, blank = False,
            verbose_name = _(u'entidad otra BD'),
            help_text = _(u'Id de la entidad descartada de la otra BD'))

    def __unicode__(self):
        return _(u'Sincr default <-> %(other_db)s [%(finished_date)s] %(other_entity_id)d') % {
                    'other_db': self.db_link_sync.db_link.other_db_name,
                    'finished_date': self.db_link_sync.finished_date.strftime('%c') if self.db_link_sync.finished_date else _(u'Actual'),
                    'other_entity_id': self.other_entity_id,
                    }

    class Meta:
	ordering = ['db_link_sync', 'other_entity_id']
	verbose_name = _(u'entidad descartada')
	verbose_name_plural = _(u'entidades descartadas')

