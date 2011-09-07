# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ViewType'
        db.create_table('Viewer_viewtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2616)),
        ))
        db.send_create_signal('Viewer', ['ViewType'])

        # Adding model 'ViewCore'
        db.create_table('Viewer_viewcore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('shortname', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=20, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2616)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Viewer.ViewType'])),
        ))
        db.send_create_signal('Viewer', ['ViewCore'])

        # Adding M2M table for field groups on 'ViewCore'
        db.create_table('Viewer_viewcore_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('viewcore', models.ForeignKey(orm['Viewer.viewcore'], null=False)),
            ('group', models.ForeignKey(orm['LabtrackerCore.group'], null=False))
        ))
        db.create_unique('Viewer_viewcore_groups', ['viewcore_id', 'group_id'])

        # Adding model 'MachineMap'
        db.create_table('Viewer_machinemap', (
            ('view', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Viewer.ViewCore'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('Viewer', ['MachineMap'])

        # Adding model 'MachineMap_Size'
        db.create_table('Viewer_machinemap_size', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2616, blank=True)),
            ('width', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('height', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('Viewer', ['MachineMap_Size'])

        # Adding model 'MachineMap_Item'
        db.create_table('Viewer_machinemap_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['LabtrackerCore.Item'])),
            ('view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Viewer.MachineMap'])),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Viewer.MachineMap_Size'])),
            ('xpos', self.gf('django.db.models.fields.IntegerField')()),
            ('ypos', self.gf('django.db.models.fields.IntegerField')()),
            ('orientation', self.gf('django.db.models.fields.CharField')(default='H', max_length=1)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('Viewer', ['MachineMap_Item'])

        # Adding unique constraint on 'MachineMap_Item', fields ['machine', 'view']
        db.create_unique('Viewer_machinemap_item', ['machine_id', 'view_id'])

        # Adding model 'InventoryList'
        db.create_table('Viewer_inventorylist', (
            ('view', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Viewer.ViewCore'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('Viewer', ['InventoryList'])

        # Adding model 'LabStats'
        db.create_table('Viewer_labstats', (
            ('view', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Viewer.ViewCore'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('Viewer', ['LabStats'])

        # Adding model 'Tags'
        db.create_table('Viewer_tags', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=60, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
        ))
        db.send_create_signal('Viewer', ['Tags'])

        # Adding model 'StatsCache'
        db.create_table('Viewer_statscache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Machine.Location'])),
            ('time_start', self.gf('django.db.models.fields.DateField')()),
            ('time_end', self.gf('django.db.models.fields.DateField')()),
            ('min_time', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
            ('max_time', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
            ('mean_time', self.gf('django.db.models.fields.FloatField')()),
            ('stdev_time', self.gf('django.db.models.fields.FloatField')()),
            ('total_time', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
            ('total_items', self.gf('django.db.models.fields.IntegerField')()),
            ('total_logins', self.gf('django.db.models.fields.IntegerField')()),
            ('total_distinct', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('Viewer', ['StatsCache'])

        # Adding M2M table for field tags on 'StatsCache'
        db.create_table('Viewer_statscache_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('statscache', models.ForeignKey(orm['Viewer.statscache'], null=False)),
            ('tags', models.ForeignKey(orm['Viewer.tags'], null=False))
        ))
        db.create_unique('Viewer_statscache_tags', ['statscache_id', 'tags_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'MachineMap_Item', fields ['machine', 'view']
        db.delete_unique('Viewer_machinemap_item', ['machine_id', 'view_id'])

        # Deleting model 'ViewType'
        db.delete_table('Viewer_viewtype')

        # Deleting model 'ViewCore'
        db.delete_table('Viewer_viewcore')

        # Removing M2M table for field groups on 'ViewCore'
        db.delete_table('Viewer_viewcore_groups')

        # Deleting model 'MachineMap'
        db.delete_table('Viewer_machinemap')

        # Deleting model 'MachineMap_Size'
        db.delete_table('Viewer_machinemap_size')

        # Deleting model 'MachineMap_Item'
        db.delete_table('Viewer_machinemap_item')

        # Deleting model 'InventoryList'
        db.delete_table('Viewer_inventorylist')

        # Deleting model 'LabStats'
        db.delete_table('Viewer_labstats')

        # Deleting model 'Tags'
        db.delete_table('Viewer_tags')

        # Deleting model 'StatsCache'
        db.delete_table('Viewer_statscache')

        # Removing M2M table for field tags on 'StatsCache'
        db.delete_table('Viewer_statscache_tags')


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
        'Machine.location': {
            'Meta': {'object_name': 'Location'},
            'building': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'floor': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'ml_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'usable_threshold': ('django.db.models.fields.IntegerField', [], {'default': '95'})
        },
        'Viewer.inventorylist': {
            'Meta': {'object_name': 'InventoryList', '_ormbases': ['Viewer.ViewCore']},
            'view': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Viewer.ViewCore']", 'unique': 'True', 'primary_key': 'True'})
        },
        'Viewer.labstats': {
            'Meta': {'object_name': 'LabStats', '_ormbases': ['Viewer.ViewCore']},
            'view': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Viewer.ViewCore']", 'unique': 'True', 'primary_key': 'True'})
        },
        'Viewer.machinemap': {
            'Meta': {'object_name': 'MachineMap', '_ormbases': ['Viewer.ViewCore']},
            'view': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Viewer.ViewCore']", 'unique': 'True', 'primary_key': 'True'})
        },
        'Viewer.machinemap_item': {
            'Meta': {'unique_together': "(('machine', 'view'),)", 'object_name': 'MachineMap_Item'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['LabtrackerCore.Item']"}),
            'orientation': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Viewer.MachineMap_Size']"}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Viewer.MachineMap']"}),
            'xpos': ('django.db.models.fields.IntegerField', [], {}),
            'ypos': ('django.db.models.fields.IntegerField', [], {})
        },
        'Viewer.machinemap_size': {
            'Meta': {'object_name': 'MachineMap_Size'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2616', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'Viewer.statscache': {
            'Meta': {'object_name': 'StatsCache'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Machine.Location']"}),
            'max_time': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'mean_time': ('django.db.models.fields.FloatField', [], {}),
            'min_time': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'stdev_time': ('django.db.models.fields.FloatField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Viewer.Tags']", 'null': 'True', 'symmetrical': 'False'}),
            'time_end': ('django.db.models.fields.DateField', [], {}),
            'time_start': ('django.db.models.fields.DateField', [], {}),
            'total_distinct': ('django.db.models.fields.IntegerField', [], {}),
            'total_items': ('django.db.models.fields.IntegerField', [], {}),
            'total_logins': ('django.db.models.fields.IntegerField', [], {}),
            'total_time': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'})
        },
        'Viewer.tags': {
            'Meta': {'object_name': 'Tags'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'})
        },
        'Viewer.viewcore': {
            'Meta': {'object_name': 'ViewCore'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2616'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['LabtrackerCore.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'shortname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Viewer.ViewType']"})
        },
        'Viewer.viewtype': {
            'Meta': {'object_name': 'ViewType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2616'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        }
    }

    complete_apps = ['Viewer']
