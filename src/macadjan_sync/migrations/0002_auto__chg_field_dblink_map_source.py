# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('macadjan', '0004_auto__add_mapsource'),
    )

    def forwards(self, orm):

        # Changing field 'DBLink.map_source'
        db.alter_column(u'macadjan_sync_dblink', 'map_source_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['macadjan.MapSource']))

    def backwards(self, orm):

        # Changing field 'DBLink.map_source'
        db.alter_column(u'macadjan_sync_dblink', 'map_source_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['macadjan_ecozoom.MapSource']))

    models = {
        u'macadjan.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marker_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'macadjan.entitytag': {
            'Meta': {'ordering': "['collection', 'name']", 'object_name': 'EntityTag'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': u"orm['macadjan.TagCollection']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'macadjan.entitytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'EntityType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'macadjan.mapsource': {
            'Meta': {'ordering': "['name']", 'object_name': 'MapSource'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        u'macadjan.subcategory': {
            'Meta': {'ordering': "['category', 'name']", 'object_name': 'SubCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategories'", 'to': u"orm['macadjan.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marker_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'macadjan.tagcollection': {
            'Meta': {'ordering': "['name']", 'object_name': 'TagCollection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'macadjan_ecozoom.ecozoomentity': {
            'Meta': {'ordering': "['name']", 'object_name': 'EcozoomEntity'},
            'additional_info': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'address_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'alias': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'contact_phone_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'contact_phone_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'contained_in': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['macadjan_ecozoom.EcozoomEntity']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'creation_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'email_2': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': u"orm['macadjan.EntityType']"}),
            'fax': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'finances': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'goals': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'how_to_access': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_container': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'legal_form': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'main_subcategory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities_main'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': u"orm['macadjan.SubCategory']"}),
            'map_source_copy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities2'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': u"orm['macadjan.MapSource']"}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'needs': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'networks_member': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'networks_works_with': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'offerings': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'ongoing_projects': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'social_values': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'subcategories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'entities'", 'blank': 'True', 'to': u"orm['macadjan.SubCategory']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'entities'", 'blank': 'True', 'to': u"orm['macadjan.EntityTag']"}),
            'web': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'web_2': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'blank': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        u'macadjan_sync.dblink': {
            'Meta': {'ordering': "['other_db_name']", 'object_name': 'DBLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_links'", 'to': u"orm['macadjan.MapSource']"}),
            'other_db_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'macadjan_sync.dblinkdiscarded': {
            'Meta': {'ordering': "['db_link_sync', 'other_entity_id']", 'object_name': 'DBLinkDiscarded'},
            'db_link_sync': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discarded'", 'to': u"orm['macadjan_sync.DBLinkSync']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_entity_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'macadjan_sync.dblinksync': {
            'Meta': {'ordering': "['db_link', 'finished_date']", 'object_name': 'DBLinkSync'},
            'db_link': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'syncs'", 'to': u"orm['macadjan_sync.DBLink']"}),
            'entities_synced': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sync_data'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['macadjan_ecozoom.EcozoomEntity']"}),
            'finished_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'macadjan_sync.entitytypematch': {
            'Meta': {'ordering': "['other_entity_type_id']", 'object_name': 'EntityTypeMatch'},
            'db_link': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entity_type_matches'", 'to': u"orm['macadjan_sync.DBLink']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_entity_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entity_type_matches'", 'to': u"orm['macadjan.EntityType']"}),
            'other_entity_type_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'macadjan_sync.subcategorymatch': {
            'Meta': {'ordering': "['local_subcategory__category__name', 'other_subcategory_slug']", 'object_name': 'SubCategoryMatch'},
            'db_link': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategory_matches'", 'to': u"orm['macadjan_sync.DBLink']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_subcategory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategory_matches'", 'to': u"orm['macadjan.SubCategory']"}),
            'other_subcategory_slug': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['macadjan_sync']
