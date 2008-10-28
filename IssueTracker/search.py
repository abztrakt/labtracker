"""
"""
import re
import operator

from django.db.models import Q 
#from django.db.models.query import QNot
from django.db import connection
#from django.db.models.query import Q
import django.forms.fields as fieldTypes
import django.forms.widgets as widgets

import LabtrackerCore.models as LabtrackerCore
import IssueTracker.models as IssueModel
from IssueTracker.forms import *
import Machine.models as Machine

def titleSearch(term):
    return IssueModel.Issue.objects.filter(title__icontains=term)

def searchFieldGen(field_name):
    """ 
    searchFieldGen

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
        # find all name spaces
        it_types = LabtrackerCore.InventoryType.objects.all()
        field.choices = []
        for group in LabtrackerCore.Group.objects.all():
            namespace = group.it.namespace
            obj = eval(namespace + ".Group")
            field.choices.extend([
                (group.pk, group.name) for group in obj.objects.all()
                ])

    return field

def parseSearch(data):
    """
    """

    # take the data and parse out what needs to be done
    keys = data.keys()
    keys.sort()

    searches = []
    keyval = re.compile(r'^(\d+)_(\w+?)(_mode)?$')
    for key, value in data.lists():
        matches = re.match(keyval, key)
        num, name, mode = matches.groups()
        num = int(num)

        if len(searches) <= num:
            searches.append({ 'name': name, })

        if mode is None:
            searches[num]['value'] = value
        else:
            searches[num]['mode'] = str(value[0])
    
    return searches

def buildQuery(searches):
    """
    """

    query = IssueModel.Issue.objects

    for search in searches:
        # take the contains and generate the search string

        term = {}
        QObjects = []
        name = str(search['name'])
        
        if search['mode'] != 'none' and name in ('assignee', 'cc', 'reporter'):
            name = "%s__username" % (name)
        elif name in ('group',):
            name = "%s__name" % (name)


        if search.has_key('value'):
            values = search['value']
        else:
            values = []

        if name in ('problem_type'):
            # we know that this is a multiselect search

            if search['mode'] == 'is':
                method = 'filter'

                if len(values) is 0:
                    # is nothing
                    QObjects.append(Q( **{ "%s__isnull" % (name) : True, } ))

                QObjects.append(Q( **{ "%s__pk__in" % (name): values, }))

            elif search['mode'] == 'is not':
                # FIXME This is broken, items that are in more than one group are returned
                # even if on the exclusion list

                # exclusion never excludes the null
                method = 'filter'
                #method = 'exclude'

                if len(values) is 0:
                    # if nothing was given, then nothing will be excluded
                    continue

                QObjects.append(Q( **{ "%s__isnull" % (name) : True, } ))
                QObjects.append(QNot(Q( **{ "%s__pk__in" % (name): values, })))

            QObject = reduce(operator.or_, QObjects)

        else:
            value = str(values[0])

            # TODO  Make pretty
        
            if search['mode'] == 'contains':
                mode = "icontains"
                method = "filter"
                QObjects.append(Q( **{ "%s__%s" % (name, mode): value, }))
            elif search['mode'] == "not contain":
                mode = "icontains" 
                method = "filter"
                QObjects.append(Q( **{ "%s__isnull" % (name) : True, } ))
                QObjects.append(QNot(Q( **{ "%s__%s" % (name, mode): value, })))
            elif search['mode'] == "is":
                mode = "iexact" 
                method = "filter"
                QObjects.append(Q( **{ "%s__%s" % (name, mode): value, }))
            elif search['mode'] == "is not":
                mode = "iexact" 
                method = "exclude"
                QObjects.append(Q( **{ "%s__%s" % (name, mode): value, }))
            elif search['mode'] == "begins with":
                method = "filter"
                mode = "istartswith" 
                QObjects.append(Q( **{ "%s__%s" % (name, mode): value, }))
            elif search['mode'] == "ends with":
                method = "filter"
                mode = "iendswith" 
                QObjects.append(Q( **{ "%s__%s" % (name, mode): value, }))
            elif search['mode'] == 'none':
                method = "filter"
                mode = "isnull"
                QObjects.append(Q( **{ "%s__%s" % (name, mode): True, }))

            #QObjects.append(Q( **{ "%s__%s" % (name, mode): value, }))

            QObject = reduce(operator.or_, QObjects)

        if method is "exclude":
            query = query.exclude( QObject )
        elif method is "filter":
            query = query.filter( QObject )


    #print connection.queries
    return query.distinct()
