"""
"""

import labtracker.LabtrackerCore.models as LabtrackerCore
from labtracker.IssueTracker.forms import *
import django.newforms.fields as fieldTypes
import django.newforms.widgets as widgets

def searchFieldGen(field_name):
    """ searchFieldGen

    Generates the field for the search term

    """

    form = SearchForm()
    field = form.fields[field_name]

    if field_name == 'resolved_state':
        field.choices = [
            (state.pk, state.name) for state in ResolveState.objects.all()]
    elif field_name == 'problem_type':
        field.choices = [
            (pt.pk, pt.name) for pt in ProblemType.objects.all()]
    elif field_name == 'inventory_type':
        field.choices = [
            (it.pk, it.name) for it in LabtrackerCore.InventoryType.objects.all()]
    elif field_name == 'assignee':
        field.choices = [
            (user.pk, user.username) for user in User.objects.all()]
    elif field_name == 'group':
        field.choices = [ ]

    return field
