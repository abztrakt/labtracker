"""
"""

from labtracker.IssueTracker.forms import *

def searchFieldGen(field_name):
    """ searchFieldGen

    Generates the field for the search term

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

    # FIXME, not working for primary_key
    #field = SearchForm().__getitem__(field_name)
    form = SearchForm()
    field = form.fields[field_name]
    field = form.__getitem__(field_name)
    #print form
    #print field
    #print form.__getitem__(field_name)
    #print dir(field)
    #print field
    #print field.widget
    #field = SearchForm().__getitem__(field_name)
    #print field
    
    import django.newforms.fields as fieldTypes
    import django.newforms.widgets as widgets

    if type(field.field.widget) is widgets.TextInput:
    #if field.widget.__class__ is widgets.TextInput:
        #print dir(field.field)
        #print field.field
        if field.__class__ is fieldTypes.IntegerField:
            field.modes = modes['int']
        else:
            field.modes = modes['text']
    elif type(field.field.widget) is widgets.SelectMultiple:
        field.modes = modes['select']
    elif type(field.field.widget) is widgets.Select:
        field.modes = modes['select']
    elif type(field.field.widget) is widgets.Textarea:
        field.modes = modes['text']

    if field_name is 'resolved_state':
        field.choices = [
            (state.pk, state.name) for state in ResolveState.objects.all()]
    elif field_name is 'problem_type':
        field.choices = [
            (pt.pk, pt.name) for pt in ProblemType.objects.all()]
    elif field_name is 'inventory_type':
        field.choices = [
            (it.pk, it.name) for it in LabtrackerCore.InventoryType.objects.all()]
    elif field_name is 'assignee':
        field.choices = [
            (user.pk, user.username) for user in User.objects.all()]

    return field
