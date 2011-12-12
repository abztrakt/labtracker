# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'LabUser'
        db.create_table('LabtrackerCore_labuser', (
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('accesses', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('LabtrackerCore', ['LabUser'])

        # Adding model 'InventoryType'
        db.create_table('LabtrackerCore_inventorytype', (
            ('inv_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('namespace', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2616)),
        ))
        db.send_create_signal('LabtrackerCore', ['InventoryType'])

        # Adding model 'Item'
        db.create_table('LabtrackerCore_item', (
            ('item_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('it', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['LabtrackerCore.InventoryType'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
        ))
        db.send_create_signal('LabtrackerCore', ['Item'])

        # Adding model 'Group'
        db.create_table('LabtrackerCore_group', (
            ('group_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('it', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['LabtrackerCore.InventoryType'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2616)),
        ))
        db.send_create_signal('LabtrackerCore', ['Group'])

        # Adding M2M table for field items on 'Group'
        db.create_table('LabtrackerCore_group_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['LabtrackerCore.group'], null=False)),
            ('item', models.ForeignKey(orm['LabtrackerCore.item'], null=False))
        ))
        db.create_unique('LabtrackerCore_group_items', ['group_id', 'item_id'])


    def backwards(self, orm):
        
        # Deleting model 'LabUser'
        db.delete_table('LabtrackerCore_labuser')

        # Deleting model 'InventoryType'
        db.delete_table('LabtrackerCore_inventorytype')

        # Deleting model 'Item'
        db.delete_table('LabtrackerCore_item')

        # Deleting model 'Group'
        db.delete_table('LabtrackerCore_group')

        # Removing M2M table for field items on 'Group'
        db.delete_table('LabtrackerCore_group_items')


    models = {
        'LabtrackerCore.group': {
            'Meta': {'object_name': 'Group'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2616'}),
            'group_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'it': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['LabtrackerCore.InventoryType']", 'null': 'True', 'blank': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['LabtrackerCore.Item']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        'LabtrackerCore.inventorytype': {
            'Meta': {'object_name': 'InventoryType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2616'}),
            'inv_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'namespace': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        'LabtrackerCore.item': {
            'Meta': {'object_name': 'Item'},
            'it': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['LabtrackerCore.InventoryType']"}),
            'item_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        'LabtrackerCore.labuser': {
            'Meta': {'object_name': 'LabUser'},
            'accesses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'})
        }
    }

    complete_apps = ['LabtrackerCore']
