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

"""
    modes = {}
    modes['text'] = [
        { 'name': 'contains', 'value': 'contains'},
        { 'name': "doesn't contain", 'value': "doesn't contain"},
        { 'name': 'is', 'value': 'is'},
        { 'name': 'is not', 'value': 'is not'},
        { 'name': 'begins with', 'value': 'begins with'},
        { 'name': 'ends with', 'value': 'ends with'},
    ]

    modes['select'] = [
        { 'name': 'is', 'value': 'is'},
        { 'name': 'is not', 'value': 'is not'},
    ]

    modes['int'] = [
        { 'name': 'is', 'value': 'is'},
        { 'name': 'is not', 'value': 'is not'},
        { 'name': 'Less than', 'value': '<'},
        { 'name': 'Greater than', 'value': '>'},
    ]
"""

# create the mode widgets

class IsOrNot(forms.widgets.TextInput):
    mode = forms.widgets.Select( choices = [ ('is', 'is'), ('is not', 'is not')])

    def render(self, name, value, attrs=None):
        return  self.mode.render("mode_%s" % name, "") + super(type(self), self).render(name, value, attrs)

class FuzzySearch(forms.widgets.TextInput):
    mode = forms.widgets.Select( choices = [ 
        ('contains', 'contains'), ('not contain', "doesn't contain"),
        ('is', 'is'), ('is not', 'is not'), ('begins with', 'begins with'),
        ('ends with', 'ends with')])

    def render(self, name, value, attrs=None):
        return  self.mode.render("mode_%s" % name, "") + super(type(self), self).render(name, value, attrs)

class IsSelected(forms.widgets.CheckboxSelectMultiple):
    mode = forms.widgets.Select( choices = [ ('is', 'is'), ('is not', 'is not')])

    def render(self, name, value, attrs=None):
        return  self.mode.render("mode_%s" % name, "") + super(type(self), self).render(name, value, attrs)



class SearchForm(forms.Form):
    """
    """
    #issue_id = STestField()
    issue_id = forms.CharField(widget=IsOrNot)
    title = forms.CharField(widget=FuzzySearch)
    description = forms.CharField(widget=FuzzySearch)
    resolve_time = forms.CharField()
    post_time = forms.CharField()
    reporter = forms.CharField(widget=FuzzySearch)
    cc = forms.CharField(widget=FuzzySearch)
    assignee = forms.CharField(widget=FuzzySearch)
    item = forms.CharField(widget=FuzzySearch)

    resolved_state = forms.MultipleChoiceField(widget = IsSelected) 
    problem_type = forms.MultipleChoiceField(widget = IsSelected) 
    group = forms.MultipleChoiceField(widget = IsSelected) # TODO choices = 
    inventory_type = forms.MultipleChoiceField(widget = IsSelected)



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
