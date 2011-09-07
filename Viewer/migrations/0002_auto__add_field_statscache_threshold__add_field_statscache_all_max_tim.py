# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'StatsCache.threshold'
        db.add_column('Viewer_statscache', 'threshold', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'StatsCache.all_max_time'
        db.add_column('Viewer_statscache', 'all_max_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2, blank=True), keep_default=False)

        # Adding field 'StatsCache.all_mean_time'
        db.add_column('Viewer_statscache', 'all_mean_time', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'StatsCache.all_total_time'
        db.add_column('Viewer_statscache', 'all_total_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2, blank=True), keep_default=False)

        # Adding field 'StatsCache.all_stdev_time'
        db.add_column('Viewer_statscache', 'all_stdev_time', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'StatsCache.threshold'
        db.delete_column('Viewer_statscache', 'threshold')

        # Deleting field 'StatsCache.all_max_time'
        db.delete_column('Viewer_statscache', 'all_max_time')

        # Deleting field 'StatsCache.all_mean_time'
        db.delete_column('Viewer_statscache', 'all_mean_time')

        # Deleting field 'StatsCache.all_total_time'
        db.delete_column('Viewer_statscache', 'all_total_time')

        # Deleting field 'StatsCache.all_stdev_time'
        db.delete_column('Viewer_statscache', 'all_stdev_time')


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
            'all_max_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'all_mean_time': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'all_stdev_time': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'all_total_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Machine.Location']"}),
            'max_time': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'mean_time': ('django.db.models.fields.FloatField', [], {}),
            'min_time': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'stdev_time': ('django.db.models.fields.FloatField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Viewer.Tags']", 'null': 'True', 'symmetrical': 'False'}),
            'threshold': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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
