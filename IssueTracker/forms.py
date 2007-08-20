from django import newforms as forms
from django.newforms import form_for_model
from labtracker.IssueTracker.models import *

CreateIssueForm = forms.form_for_model(Issue,
        fields=('it','group','item','cc','problem_type','title','description','reporter'))

UpdateIssueForm = forms.form_for_model(Issue,
        fields=('issue_id','assignee','cc','resolve_time',
            'resolved_state', 'last_modified'))

AddCommentForm = forms.form_for_model(IssuePost,
        fields=('issue', 'user','comment'))

