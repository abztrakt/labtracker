from django import newforms as forms
from django.newforms import form_for_model
from django.newforms.forms import BaseForm, SortedDictFromList
from labtracker.IssueTracker.models import *

#IssueForm = forms.form_for_model(Issue, formfield_callback=issueCallback)
IssueForm = forms.form_for_model(Issue)

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
    issue_id = forms.CharField(label="Issue ID", widget=IsOrNot)
    title = forms.CharField(label="Title", widget=FuzzySearch)
    description = forms.CharField(label="Description", widget=FuzzySearch)
    resolve_time = forms.CharField(label="Resolved Time")
    post_time = forms.CharField(label="Posted Time")
    reporter = forms.CharField(label="Reporter", widget=FuzzySearch)
    cc = forms.CharField(label='CC', widget=FuzzySearch)
    assignee = forms.CharField(label='Assignee', widget=FuzzySearch)
    item = forms.CharField(label='Item', widget=FuzzySearch)

    resolved_state = forms.MultipleChoiceField(label="Resolved State", widget =
            IsSelected(attrs={'class':'inline struct'})) 
    problem_type = forms.MultipleChoiceField(label="Problem Type", widget =
            IsSelected(attrs={'class':'inline struct'})) 
    group = forms.MultipleChoiceField(label="Group", widget =
            IsSelected(attrs={'class':'inline struct'})) # TODO choices = 
    inventory_type = forms.MultipleChoiceField(label="Inventory Type", widget =
            IsSelected(attrs={'class':'inline struct'}))



# like IssueForm, but with the primary key as well
#SearchForm = forms.form_for_model(Issue, 
        #formfield_callback = lambda f: (f.formfield(), forms.CharField())[f.primary_key])

#searchFormFields = [ 
        #(field.name, field.verbose_name.capitalize()) \
                #for field in Issue._meta.fields 
    #] + [
        #(field.name, field.verbose_name.capitalize()) \
                #for field in Issue._meta.many_to_many 
    #]

searchFormFields = [ 
        (field, SearchForm.__dict__['base_fields'][field].label) \
                for field in SearchForm.__dict__['base_fields']
    ]
searchFormFields.sort()
#print searchFormFields

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
