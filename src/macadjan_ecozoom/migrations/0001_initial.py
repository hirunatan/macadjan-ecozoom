# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MapSource'
        db.create_table('macadjan_ecozoom_mapsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('web', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
        ))
        db.send_create_signal('macadjan_ecozoom', ['MapSource'])

        # Adding model 'EcozoomEntity'
        db.create_table('macadjan_ecozoom_ecozoomentity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, db_index=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('is_container', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contained_in', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['macadjan_ecozoom.EcozoomEntity'], null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(max_length=100, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(max_length=100, null=True, blank=True)),
            ('address_1', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('address_2', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(default='', max_length=5, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('zone', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('contact_phone_1', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('contact_phone_2', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True)),
            ('email_2', self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True)),
            ('web', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
            ('web_2', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
            ('contact_person', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('entity_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entities', null=True, to=orm['macadjan.EntityType'])),
            ('main_subcategory', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entities_main', null=True, to=orm['macadjan.SubCategory'])),
            ('creation_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('legal_form', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('goals', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('finances', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('social_values', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('how_to_access', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('networks_member', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('networks_works_with', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('ongoing_projects', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('needs', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('offerings', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('additional_info', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('map_source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entities', null=True, to=orm['macadjan_ecozoom.MapSource'])),
        ))
        db.send_create_signal('macadjan_ecozoom', ['EcozoomEntity'])

        # Adding M2M table for field subcategories on 'EcozoomEntity'
        db.create_table('macadjan_ecozoom_ecozoomentity_subcategories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ecozoomentity', models.ForeignKey(orm['macadjan_ecozoom.ecozoomentity'], null=False)),
            ('subcategory', models.ForeignKey(orm['macadjan.subcategory'], null=False))
        ))
        db.create_unique('macadjan_ecozoom_ecozoomentity_subcategories', ['ecozoomentity_id', 'subcategory_id'])

        # Adding M2M table for field tags on 'EcozoomEntity'
        db.create_table('macadjan_ecozoom_ecozoomentity_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ecozoomentity', models.ForeignKey(orm['macadjan_ecozoom.ecozoomentity'], null=False)),
            ('entitytag', models.ForeignKey(orm['macadjan.entitytag'], null=False))
        ))
        db.create_unique('macadjan_ecozoom_ecozoomentity_tags', ['ecozoomentity_id', 'entitytag_id'])


    def backwards(self, orm):
        
        # Deleting model 'MapSource'
        db.delete_table('macadjan_ecozoom_mapsource')

        # Deleting model 'EcozoomEntity'
        db.delete_table('macadjan_ecozoom_ecozoomentity')

        # Removing M2M table for field subcategories on 'EcozoomEntity'
        db.delete_table('macadjan_ecozoom_ecozoomentity_subcategories')

        # Removing M2M table for field tags on 'EcozoomEntity'
        db.delete_table('macadjan_ecozoom_ecozoomentity_tags')


    models = {
        'macadjan.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marker_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'macadjan.entitytag': {
            'Meta': {'ordering': "['collection', 'name']", 'object_name': 'EntityTag'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': "orm['macadjan.TagCollection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'macadjan.entitytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'EntityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'macadjan.subcategory': {
            'Meta': {'ordering': "['category', 'name']", 'object_name': 'SubCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subcategories'", 'to': "orm['macadjan.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marker_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'macadjan.tagcollection': {
            'Meta': {'ordering': "['name']", 'object_name': 'TagCollection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'macadjan_ecozoom.ecozoomentity': {
            'Meta': {'ordering': "['name']", 'object_name': 'EcozoomEntity'},
            'additional_info': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'address_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'alias': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'contact_phone_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'contact_phone_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'contained_in': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['macadjan_ecozoom.EcozoomEntity']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'creation_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'email_2': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities'", 'null': 'True', 'to': "orm['macadjan.EntityType']"}),
            'fax': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'finances': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'goals': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'how_to_access': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_container': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'legal_form': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'main_subcategory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities_main'", 'null': 'True', 'to': "orm['macadjan.SubCategory']"}),
            'map_source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities'", 'null': 'True', 'to': "orm['macadjan_ecozoom.MapSource']"}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'needs': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'networks_member': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'networks_works_with': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'offerings': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'ongoing_projects': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'social_values': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'subcategories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'entities'", 'blank': 'True', 'to': "orm['macadjan.SubCategory']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'entities'", 'blank': 'True', 'to': "orm['macadjan.EntityTag']"}),
            'web': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'web_2': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'blank': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        'macadjan_ecozoom.mapsource': {
            'Meta': {'ordering': "['name']", 'object_name': 'MapSource'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['macadjan_ecozoom']
