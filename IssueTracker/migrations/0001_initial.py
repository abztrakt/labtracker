# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ResolveState'
        db.create_table('IssueTracker_resolvestate', (
            ('rs_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400)),
        ))
        db.send_create_signal('IssueTracker', ['ResolveState'])

        # Adding model 'ProblemType'
        db.create_table('IssueTracker_problemtype', (
            ('pb_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400)),
        ))
        db.send_create_signal('IssueTracker', ['ProblemType'])

        # Adding M2M table for field inv on 'ProblemType'
        db.create_table('IssueTracker_problemtype_inv', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('problemtype', models.ForeignKey(orm['IssueTracker.problemtype'], null=False)),
            ('inventorytype', models.ForeignKey(orm['LabtrackerCore.inventorytype'], null=False))
        ))
        db.create_unique('IssueTracker_problemtype_inv', ['problemtype_id', 'inventorytype_id'])

        # Adding model 'Issue'
        db.create_table('IssueTracker_issue', (
            ('issue_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('it', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['LabtrackerCore.InventoryType'], null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['LabtrackerCore.Group'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['LabtrackerCore.Item'])),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reporter', to=orm['auth.User'])),
            ('assignee', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assignee', null=True, to=orm['auth.User'])),
            ('post_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('resolve_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('resolved_state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['IssueTracker.ResolveState'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('IssueTracker', ['Issue'])

        # Adding M2M table for field cc on 'Issue'
        db.create_table('IssueTracker_email_cc', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issue', models.ForeignKey(orm['IssueTracker.issue'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('IssueTracker_email_cc', ['issue_id', 'user_id'])

        # Adding M2M table for field problem_type on 'Issue'
        db.create_table('IssueTracker_issue_problem_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issue', models.ForeignKey(orm['IssueTracker.issue'], null=False)),
            ('problemtype', models.ForeignKey(orm['IssueTracker.problemtype'], null=False))
        ))
        db.create_unique('IssueTracker_issue_problem_type', ['issue_id', 'problemtype_id'])

        # Adding model 'IssueHistory'
        db.create_table('IssueTracker_issuehistory', (
            ('ih_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['IssueTracker.Issue'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('IssueTracker', ['IssueHistory'])

        # Adding model 'IssueComment'
        db.create_table('IssueTracker_issuecomment', (
            ('ip_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['IssueTracker.Issue'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('IssueTracker', ['IssueComment'])


    def backwards(self, orm):
        
        # Deleting model 'ResolveState'
        db.delete_table('IssueTracker_resolvestate')

        # Deleting model 'ProblemType'
        db.delete_table('IssueTracker_problemtype')

        # Removing M2M table for field inv on 'ProblemType'
        db.delete_table('IssueTracker_problemtype_inv')

        # Deleting model 'Issue'
        db.delete_table('IssueTracker_issue')

        # Removing M2M table for field cc on 'Issue'
        db.delete_table('IssueTracker_email_cc')

        # Removing M2M table for field problem_type on 'Issue'
        db.delete_table('IssueTracker_issue_problem_type')

        # Deleting model 'IssueHistory'
        db.delete_table('IssueTracker_issuehistory')

        # Deleting model 'IssueComment'
        db.delete_table('IssueTracker_issuecomment')


    models = {
        'IssueTracker.issue': {
            'Meta': {'object_name': 'Issue'},
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assignee'", 'null': 'True', 'to': "orm['auth.User']"}),
            'cc': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cc_user'", 'to': "orm['auth.User']", 'db_table': "'IssueTracker_email_cc'", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['LabtrackerCore.Group']"}),
            'issue_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'it': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['LabtrackerCore.InventoryType']", 'null': 'True', 'blank': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['LabtrackerCore.Item']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'problem_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['IssueTracker.ProblemType']", 'null': 'True', 'blank': 'True'}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reporter'", 'to': "orm['auth.User']"}),
            'resolve_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'resolved_state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['IssueTracker.ResolveState']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'IssueTracker.issuecomment': {
            'Meta': {'object_name': 'IssueComment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'ip_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['IssueTracker.Issue']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'IssueTracker.issuehistory': {
            'Meta': {'object_name': 'IssueHistory'},
            'ih_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['IssueTracker.Issue']"}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'IssueTracker.problemtype': {
            'Meta': {'object_name': 'ProblemType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'inv': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['LabtrackerCore.InventoryType']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'pb_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'IssueTracker.resolvestate': {
            'Meta': {'object_name': 'ResolveState'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'rs_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
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

    complete_apps = ['IssueTracker']
