# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for item in orm.Item.objects.all():
            try:
                item.status.get(name='Usable')
            except ObjectDoesNotExist:
                item.unusable = True
                item.save()


    def backwards(self, orm):
        "Write your backwards methods here."
        try:
            usable = orm.Status.objects.get(name='Usable')
        except ObjectDoesNotExist:
            usable = orm.Status(name='Usable', description='This machine is usable.')
            usable.save()

        usable = orm.Status.obejcts.get(name='Usable')
        for i in orm.item.obejcts.all():
            if not i.unusable:
                i.status.add(usable)
                i.save()


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
        },
        'Machine.contact': {
            'Meta': {'object_name': 'Contact'},
            'contact_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mg': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Machine.Group']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'Machine.group': {
            'Meta': {'object_name': 'Group', '_ormbases': ['LabtrackerCore.Group']},
            'casting_server': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'core': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['LabtrackerCore.Group']", 'unique': 'True', 'primary_key': 'True'}),
            'gateway': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'is_lab': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Machine.history': {
            'Meta': {'object_name': 'History'},
            'login_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Machine.Item']"}),
            'mh_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['Machine.Status']", 'null': 'True', 'blank': 'True'}),
            'session_time': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['LabtrackerCore.LabUser']"})
        },
        'Machine.item': {
            'Meta': {'object_name': 'Item', '_ormbases': ['LabtrackerCore.Item']},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'core': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['LabtrackerCore.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Machine.Location']"}),
            'mac1': ('Machine.models.MacField', [], {}),
            'mac2': ('Machine.models.MacField', [], {'blank': 'True'}),
            'mac3': ('Machine.models.MacField', [], {'blank': 'True'}),
            'manu_tag': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'purchase_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'machine_status'", 'symmetrical': 'False', 'to': "orm['Machine.Status']"}),
            'stf_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Machine.Type']"}),
            'unusable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uw_tag': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wall_port': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'warranty_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'Machine.location': {
            'Meta': {'object_name': 'Location'},
            'building': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'floor': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ml_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'usable_threshold': ('django.db.models.fields.IntegerField', [], {'default': '95'})
        },
        'Machine.platform': {
            'Meta': {'object_name': 'Platform'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'platform_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Machine.status': {
            'Meta': {'unique_together': "(('ms_id', 'name'),)", 'object_name': 'Status'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'ms_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'})
        },
        'Machine.type': {
            'Meta': {'object_name': 'Type'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'mt_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Machine.Platform']"}),
            'specs': ('django.db.models.fields.TextField', [], {})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Machine']
