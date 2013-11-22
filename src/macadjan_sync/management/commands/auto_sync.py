# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from macadjan import models
from macadjan_sync import models as models_sync


class SyncException(Exception):
    pass

class Command(BaseCommand):
    args = 'remote_db_name'
    help = '''
           Synchronize automatically with a remote database (accept all remote changes).
           '''

    def handle(self, *args, **options):
        if len(args) == 0:
            print u'Usage: ./manage.py auto_sync <remote_db_name>'
            exit(1)

        remote_db_name = args[0]

        print u'Automatic sync with db %s' % remote_db_name
        self.auto_sync(remote_db_name)

    def auto_sync(self, remote_db_name):
        db_link = models_sync.DBLink.objects.get(other_db_name = remote_db_name)

        (grouped_list, synced_entities, discarded_entities) = db_link.sync_entity_lists()
        for (subcategory_name, new_entities, modified_entities, conflict_entities) in grouped_list:
            print u'Syncing %s' % subcategory_name
            self.sync_new_entities(db_link, subcategory_name, new_entities)
            self.sync_modified_entities(db_link, subcategory_name, modified_entities)
            self.sync_modified_entities(db_link, subcategory_name, conflict_entities)

        db_link.finish_sync()
        db_link.save()

    def sync_new_entities(self, db_link, subcategory_name, new_entities):
        for new_entity in new_entities:
            print u'  -> Creating %s' % new_entity.name
            (other_entity_type, matching_entity_types) = db_link.get_matching_entity_types(new_entity)
            (other_subcategories, matching_subcategories) = db_link.get_matching_subcategories(new_entity)

            if len(matching_entity_types) == 0:
                raise SyncException('Remote type %s does not have any matching type in this db' % other_entity_type)
            new_entity_type = matching_entity_types[0]

            new_subcategories = []
            new_main_subcategory = None
            for other_subcategory, matching_subcategory in zip(other_subcategories, matching_subcategories):
                if len(matching_subcategory) == 0:
                    raise SyncException('Remote subcategory %s does not have any matching subcategory in this db' % other_subcategory)
                new_subcategories.append(matching_subcategory[0])
                if new_entity.main_subcategory == other_subcategory:
                    new_main_subcategory = matching_subcategory[0]

            if len(new_subcategories) == 0:
                raise SyncException('Remote entity %s does not have any subcategory' % new_entity.name)

            if not new_main_subcategory:
                new_main_subcategory = new_subcategories[0]

            db_link.create_local_entity(new_entity, new_entity_type, new_main_subcategory, new_subcategories)
            db_link.mark_synced_entity(new_entity)

    def sync_modified_entities(self, db_link, subcategory_name, modified_entities):
        for entity_local, entity_other in modified_entities:
            print u'  -> Updating %s' % entity_local.name
            for field_name in entity_local._meta.get_all_field_names():

                if field_name in ['id', 'ecozoomentity', 'change_proposals', 'sync_data', 'tags', 'contained_in']:
                    continue

                local_value = getattr(entity_local, field_name)
                if field_name == 'map_source':
                    other_value = db_link.map_source
                elif field_name == 'entity_type':
                    (other_entity_type, matching_entity_types) = db_link.get_matching_entity_types(entity_other)
                    if len(matching_entity_types) == 0:
                        raise SyncException('Remote type %s does not have any matching type in this db' % other_entity_type)
                    other_value = matching_entity_types[0]
                elif field_name == 'main_subcategory':
                    (other_subcategories, matching_subcategories) = db_link.get_matching_subcategories(entity_other)

                    new_subcategories = []
                    new_main_subcategory = None
                    for other_subcategory, matching_subcategory in zip(other_subcategories, matching_subcategories):
                        if len(matching_subcategory) == 0:
                            raise SyncException('Remote subcategory %s does not have any matching subcategory in this db' % other_subcategory)
                        new_subcategories.append(matching_subcategory[0])
                        if entity_other.main_subcategory == other_subcategory:
                            new_main_subcategory = matching_subcategory[0]

                    other_value = new_main_subcategory

                    entity_local.subcategories.clear()
                    for category in new_subcategories:
                        entity_local.subcategories.add(category)
                elif field_name == 'subcategories':
                    continue
                else:
                    other_value = getattr(entity_other, field_name)

                #print u' [{}] <- "%s"' % [field_name, unicode(other_value)[:100]]
                setattr(entity_local, field_name, other_value)

            entity_local.save(update_dates = False)
            db_link.mark_synced_entity(entity_local)

