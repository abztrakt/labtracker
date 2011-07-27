from django.contrib.auth.models import User
from django import forms, dispatch
from django.forms import ModelForm
from django.forms.forms import BaseForm      #, SortedDictFromList
from IssueTracker import changedIssueSignal
import IssueTracker.models as im
import LabtrackerCore.models as lm

# Not using these strings, currently setting the fields to empty strings. Might change in future.
DEFAULT_DESCRIPTION = """Description of Problem:

What was the expected behavior/output? What did you observe?

"""

DEFAULT_STEPS = """What are the steps to reproduce the problem (if reproducible)?
 1. 
 2.
 3.
"""

DEFAULT_ATTEMPTS = """
Have you attempted to fix the problem? How?
"""


class CreateIssueForm(ModelForm):
    """
    This form is used for creating issues
    """
    it = forms.ModelChoiceField(
            queryset = lm.InventoryType.objects.all(),
            initial = lm.InventoryType.objects.all()[0],
            label = "Type"
        )

    problem_type = forms.ModelMultipleChoiceField(
            queryset=im.ProblemType.objects.all().order_by('name'),
            help_text="Select one or more problems"
        )

    description = forms.CharField(
            widget = forms.Textarea,
            initial = ""
        )

    steps = forms.CharField(
            widget = forms.Textarea,
            initial = ""
        )

    attempts = forms.CharField(
            widget = forms.Textarea,
            initial = ""
        )

    def save(self, *args, **kwargs):
        inst = ModelForm.save(self, *args, **kwargs)

        return inst

    class Meta:
        model = im.Issue
        fields = ('it','group','item','assignee','cc','problem_type','title','description',
                'reporter','steps','attempts')

class UpdateIssueForm(ModelForm):
    """
    This form is used for updating issue

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
        #import pdb; pdb.set_trace()
        for key in all_keys.difference(given_keys):
            del cleaned_data[key]
        return cleaned_data

    def save(self, *args, **kwargs):
        changedIssueSignal.send(sender=self.instance, data=self.data)
        inst = ModelForm.save(self, *args, **kwargs)

    class Meta:
        model = im.Issue
        fields = ['problem_type','assignee','cc','resolve_time', 'resolved_state', 
                'last_modified']

class AddCommentForm(ModelForm):
    """
    This form is used for adding comments to issues
    """
    class Meta:
        model = im.IssueComment
        fields = ['issue', 'user','comment']
