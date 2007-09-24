from django import newforms as forms
from django.newforms import form_for_model
from django.newforms.forms import BaseForm, SortedDictFromList
from labtracker.IssueTracker.models import *

#IssueForm = forms.form_for_model(Issue, formfield_callback=issueCallback)
IssueForm = forms.form_for_model(Issue)

searchFormFields = [ 
        (field.name, field.verbose_name.capitalize()) \
                for field in Issue._meta.fields 
    ] + [
        (field.name, field.verbose_name.capitalize()) \
                for field in Issue._meta.many_to_many 
    ]
searchFormFields.sort()

# choices

class SearchForm(forms.Form):
    """
    """
    issue_id = forms.CharField()
    title = forms.CharField()
    description = forms.CharField()
    resolve_time = forms.CharField()
    post_time = forms.CharField()
    reporter = forms.CharField()
    cc = forms.CharField()

    resolved_state = forms.MultipleChoiceField(widget = forms.widgets.CheckboxSelectMultiple) 
    problem_type = forms.MultipleChoiceField(widget = forms.widgets.CheckboxSelectMultiple) 
    group = forms.MultipleChoiceField(widget = forms.widgets.CheckboxSelectMultiple) # TODO choices = 
    inventory_type = forms.MultipleChoiceField(widget = forms.widgets.CheckboxSelectMultiple)

    assignee = forms.MultipleChoiceField() # TODO choices = 
    item = forms.MultipleChoiceField() # TODO choices = 


# like IssueForm, but with the primary key as well
#SearchForm = forms.form_for_model(Issue, 
        #formfield_callback = lambda f: (f.formfield(), forms.CharField())[f.primary_key])

class AddSearchForm(forms.Form):
    """
    A drop down list of searchable formfields
    """
    fields = forms.ChoiceField(
            choices = searchFormFields
        )

CreateIssueForm = forms.form_for_model(Issue,
        fields=('it','group','item','cc','problem_type','title','description','reporter'))

UpdateIssueForm = forms.form_for_model(Issue,
        fields=('issue_id','assignee','cc','resolve_time',
            'resolved_state', 'last_modified'))

AddCommentForm = forms.form_for_model(IssuePost,
        fields=('issue', 'user','comment'))
