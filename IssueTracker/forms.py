from django.contrib.auth.models import User
from django import forms, dispatch
from django.forms import ModelForm
from django.forms.forms import BaseForm      #, SortedDictFromList

from IssueTracker import newIssueSignal
import IssueTracker.models as im

class CreateIssueForm(ModelForm):
    """
    This form is used for creating issues
    """
    def save(self, *args, **kwargs):
        inst = ModelForm.save(self, *args, **kwargs)

        # send signal
        newIssueSignal.send(sender=self, instance=inst)

        return inst

    class Meta:
        model = im.Issue
        fields = ('it','group','item','cc','problem_type','title','description',
                'reporter')

class UpdateIssueForm(ModelForm):
    """
    This form is used for updating issues

    This form will only update items *explicitily* given to it
    """
    def clean(self):
        """
        for any fields that don't have an entry, default to old value.
        only update if *explicitly* given
        """

        cleaned_data = self.cleaned_data

        given_keys = set(self.data.keys())
        all_keys = set(cleaned_data.keys())

        # get keys that not given, delete them from cleaned_data
        for key in all_keys.difference(given_keys):
            del cleaned_data[key]

        return cleaned_data

    class Meta:
        model = im.Issue
        fields = ('problem_type','assignee','cc','resolve_time', 'resolved_state', 
                'last_modified')

class AddCommentForm(ModelForm):
    """
    This form is used for adding comments to issues
    """
    class Meta:
        model = im.IssueComment
        fields = ('issue', 'user','comment')
