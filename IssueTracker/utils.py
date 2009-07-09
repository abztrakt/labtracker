from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from IssueTracker.models import *
import LabtrackerCore.models as LabtrackerCore
import LabtrackerCore.utils
class IssueHooks(object):
    """
    Maintains a set of hooks for inventory types

    These hooks will be called on create/createSubmit/view/update
    """
    
    def __init__(self):
        """
        """

        # hook storage is done through a dictionary
        # format is { inventoryType: function }

        self.hooks = {
            'create': {},
            'createSubmit': {},
            'view': {},
            'update': {},
            'updateSubmit': {},
            'updateForm': {},
        }

    def registerHook(self, type, inv_t, f):
        self.hooks[type][inv_t] = f

    def getHook(self, type, inv_t):
        if not self.hooks.has_key(type):
            return None

        dict = self.hooks[type]

        if dict.has_key(inv_t):
            return dict[inv_t]

        return None

    def getCreateHook(self, inv_t):
        return self.getHook('create', inv_t)

    def getCreateSubmitHook(self, inv_t):
        return self.getHook('createSubmit', inv_t)

    def getViewHook(self, inv_t):
        return self.getHook('view', inv_t)

    def getUpdateSubmitHook(self, inv_t):
        return self.getHook('updateSubmit', inv_t)

    def getUpdateHook(self, inv_t):
        return self.getHook('update', inv_t)

issueHooks = IssueHooks()

def issueHook(type, **kwargs):
    """
    Decorator to simplify way to register issue hooks
    """
    def decorate(f):
        inv_t =  f.__module__.split('.')[-2]
        issueHooks.registerHook(type, inv_t, f)

        return f
    return decorate

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

def generateIssueArgs(request, qdict):
    return LabtrackerCore.utils.generateOrderingArgs(request, qdict)
    """
    Create issue args for rendering a view issue form
    (Ported to LabtrackerCore.utils)
    """

def generatePageList(request, qdict, page_num):
    return LabtrackerCore.utils.generatePageList(request, qdict, page_num)
    """
    Generates args needed for issue_list template
    Take some arguments from user in data, the page number to show and the 
    returned query items, render out to user
    (Ported to LabtrackerCore.utils)
    """

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
