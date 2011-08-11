# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Status'
        db.create_table('Machine_status', (
            ('ms_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=60, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
        ))
        db.send_create_signal('Machine', ['Status'])

        # Adding unique constraint on 'Status', fields ['ms_id', 'name']
        db.create_unique('Machine_status', ['ms_id', 'name'])

        # Adding model 'Platform'
        db.create_table('Machine_platform', (
            ('platform_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
        ))
        db.send_create_signal('Machine', ['Platform'])

        # Adding model 'Type'
        db.create_table('Machine_type', (
            ('mt_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Machine.Platform'])),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('specs', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
        ))
        db.send_create_signal('Machine', ['Type'])

        # Adding model 'Location'
        db.create_table('Machine_location', (
            ('ml_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('building', self.gf('django.db.models.fields.CharField')(max_length=60, null=True)),
            ('floor', self.gf('django.db.models.fields.SmallIntegerField')(null=True)),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=600)),
        ))
        db.send_create_signal('Machine', ['Location'])

        # Adding model 'Item'
        db.create_table('Machine_item', (
            ('core', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['LabtrackerCore.Item'], unique=True, primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Machine.Type'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Machine.Location'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('mac1', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('mac2', self.gf('django.db.models.fields.CharField')(max_length=17, null=True, blank=True)),
            ('wall_port', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('manu_tag', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('uw_tag', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('purchase_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('warranty_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('stf_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('Machine', ['Item'])

        # Adding M2M table for field status on 'Item'
        db.create_table('Machine_item_status', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['Machine.item'], null=False)),
            ('status', models.ForeignKey(orm['Machine.status'], null=False))
        ))
        db.create_unique('Machine_item_status', ['item_id', 'status_id'])

        # Adding model 'Group'
        db.create_table('Machine_group', (
            ('core', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['LabtrackerCore.Group'], unique=True, primary_key=True)),
            ('is_lab', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('casting_server', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('gateway', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal('Machine', ['Group'])

        # Adding model 'History'
        db.create_table('Machine_history', (
            ('mh_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Machine.Item'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['LabtrackerCore.LabUser'])),
            ('session_time', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2, blank=True)),
            ('login_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('Machine', ['History'])

        # Adding M2M table for field ms on 'History'
        db.create_table('Machine_history_ms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('history', models.ForeignKey(orm['Machine.history'], null=False)),
            ('status', models.ForeignKey(orm['Machine.status'], null=False))
        ))
        db.create_unique('Machine_history_ms', ['history_id', 'status_id'])

        # Adding model 'Contact'
        db.create_table('Machine_contact', (
            ('contact_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mg', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Machine.Group'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Machine', ['Contact'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Status', fields ['ms_id', 'name']
        db.delete_unique('Machine_status', ['ms_id', 'name'])

        # Deleting model 'Status'
        db.delete_table('Machine_status')

        # Deleting model 'Platform'
        db.delete_table('Machine_platform')

        # Deleting model 'Type'
        db.delete_table('Machine_type')

        # Deleting model 'Location'
        db.delete_table('Machine_location')

        # Deleting model 'Item'
        db.delete_table('Machine_item')

        # Removing M2M table for field status on 'Item'
        db.delete_table('Machine_item_status')

        # Deleting model 'Group'
        db.delete_table('Machine_group')

        # Deleting model 'History'
        db.delete_table('Machine_history')

        # Removing M2M table for field ms on 'History'
        db.delete_table('Machine_history_ms')

        # Deleting model 'Contact'
        db.delete_table('Machine_contact')


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
            'ms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Machine.Status']", 'null': 'True', 'symmetrical': 'False'}),
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
            'mac1': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'mac2': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'manu_tag': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'purchase_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'machine_status'", 'symmetrical': 'False', 'to': "orm['Machine.Status']"}),
            'stf_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Machine.Type']"}),
            'uw_tag': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'wall_port': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'warranty_date': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        'Machine.location': {
            'Meta': {'object_name': 'Location'},
            'building': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'floor': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'ml_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
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
