# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.template.defaultfilters import slugify

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for item in orm.item.objects.all():
            item.slug=slugify(item.name)
            item.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        pass

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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60', 'db_index': 'True'})
        },
        'LabtrackerCore.labuser': {
            'Meta': {'object_name': 'LabUser'},
            'accesses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'})
        }
    }

    complete_apps = ['LabtrackerCore']
