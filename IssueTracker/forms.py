from django import newforms as forms
from django.newforms import form_for_model
from labtracker.IssueTracker.models import *

"""
class NewIssueForm(forms.Form):
    title = forms.CharField(max_length=200)
"""

CreateIssueForm = forms.form_for_model(Issue,
        #fields=('it','cc','problem_type','title','description','reporter'))
        fields=('it','group','item','cc','problem_type','title','description','reporter'))

class NewIssueForm(CreateIssueForm):
    group = forms.MultipleChoiceField([])
    item = forms.MultipleChoiceField([])

UpdateIssueForm = forms.form_for_model(Issue,
        fields=('issue_id','assignee','cc','resolve_time',
            'resolved_state', 'last_modified'))

AddCommentForm = forms.form_for_model(IssuePost,
        fields=('issue', 'user','comment'))
