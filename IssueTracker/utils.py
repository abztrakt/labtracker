from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from IssueTracker.models import *
import LabtrackerCore.models as LabtrackerCore

def updateHistory(user, issue, msg):
    history = IssueHistory(user=user,message=msg,issue=issue)
    history.save()

def modelsToDicts(items):
    """
    Takes a list of items and turns each one into a dict, then returns the list of dicts
    """
    list = []
    for item in items:
        list.append(forms.models.model_to_dict( item ))
    return list

def createGroupList(inv_ids, field='Group'):
    list = {}

    for inv_id in inv_ids:
        # fetch groups with that invtype
        groups = LabtrackerCore.Group.objects.filter(it=inv_id)

        for group in groups:
            data = forms.models.model_to_dict(group)
            data['name'] = group.name
            list[group.group_id] = data
    return list

def createItemDict(items, field='Item'):
    """
    Takes a set of items and creates a dictionary out of the items
    """
    list = {}

    for item in items:
        data = forms.models.model_to_dict(item.item)
        data['name'] = item.name
        for key in data.keys():
            if type(data[key]) not in (int, float, unicode, str):
                data.__delitem__(key)
        list[item.item.item_id] = data

    return list

def generatePageList(request, qdict, page_num):
    """
    Generates args needed for issue_list template
    Take some arguments from user in data, the page number to show and the 
    returned query items, render out to user
    """

    data = request.GET.copy()

    # TODO need user-defined limits
    num_per_page = 30

    orderby = data.get('orderby', 'issue_id')
    omethod = data.get('ometh', 'ASC')
    order_symbol = ('-', '')[omethod == 'ASC']

    issues = qdict.order_by(order_symbol + orderby)

    p = Paginator(issues, 30)

    args = {
            'orderby':  orderby,
            'omethod':  ('ASC', 'DESC')[omethod=='ASC'],
            'page':     p.page(page_num),
            'search_term':  data.get('search_term')
        }


    if args['search_term']:
        # kludgy way of doing things
        args['extraArgs'] = '&search_term=%s' % ( args['search_term'] )

    return args

def getIssueContacts(instance):
    """
    Given instance of an issue, attempt to retrieve contacts
    """
    if instance.group == None and instance.item == None:
        return

    contacts = []

    if instance.group:
        g_contacts = instance.group.group.primaryContact()
        contacts = [contact.user for contact in g_contacts]

    contacts = set(contacts)

    # now add contacts for item groups
    if instance.item:
        i_contacts = instance.item.item.primaryContact()
        contacts = contacts.union([c.user for c in i_contacts])

    return contacts
