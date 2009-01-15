from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404

import simplejson

import IssueTracker.search as issueSearch
import LabtrackerCore.models as cm
import IssueTracker.utils as utils
from IssueTracker.models import Issue

@permission_required('IssueTracker.add_issue')
def getSearchField(request, field_name):
    """ 
    Retrieves a search field and returns it in JSON
    """
    field = issueSearch.searchFieldGen(field_name)

    # TODO some better escaping needs to be done
    return HttpResponse("{ 'label': '%s', 'field': '%s' }" % \
            (field.label, field.widget.render(field_name, "").replace("\n", "")))

@permission_required('IssueTracker.can_view', login_url="/issue/login/")
def userCheck(request, name):
    """
    Given a username, check to see if the user exists, returns user info
    """

    resp = { 'exists' : 0, }
    try:
        user = User.objects.get(username=name)
        resp['id'] = user.id
        resp['active'] = user.is_active
        resp['username'] = user.username
        resp['email'] = user.email
        resp['exists'] = 1
    except ObjectDoesNotExist, e:
        resp['exists'] = 0

    return HttpResponse(simplejson.dumps(resp))

@permission_required('IssueTracker.add_issue')
def getItems(request):
    """
    Given a group id, will return a list of items that belongs to that group
    """

    data = request.REQUEST.copy()
    group_ids = data.getlist('group_id')

    items = {}
    contacts = set()
    # fetch the groups
    if len(group_ids) == 0 or "" in group_ids:
        # fetch all groups
        items = utils.createItemDict(
            cm.Item.objects.order_by('it'))
    else:
        groups = cm.Group.objects.in_bulk(group_ids).values()

        # for each group, get all the items
        # we will also return the primary contact for the group
        for group in groups:
            items.update(utils.createItemDict(group.items.all()))
            cons = group.group.primaryContact()
            contacts = contacts.union(set([c.user.username for c in cons]))

    # get the items in the group
    type = data.get("type", "json")

    dict = {
        "contacts": [c for c in contacts],
        "items": items,
    }

    if type == "xml":
        # TODO XML serialization
        pass
    else:
        return HttpResponse(simplejson.dumps(dict))

@permission_required('IssueTracker.add_issue')
def getGroups(request):
    """
    Given an inventory type, will return a list of groups that belongs to that
    inventory_type
    """
    data = request.REQUEST.copy()

    if not data.has_key('it_id'):
        it_types = []
    else:
        it_types = data.getlist('it_id')
    
    groups = []
    if len(it_types) == 0 or "" in it_types:
        # get all groups
        groups = utils.createGroupList(cm.InventoryType.objects.all())
    else:
        groups = utils.createGroupList(
            cm.InventoryType.objects.in_bulk(it_types).values())

    type = data.get("type", "json")
    
    if type == "xml":
        # TODO XML serialization
        pass
    elif type == "json":
        return HttpResponse(simplejson.dumps(groups))
    else:
        return HttpResponseNotFound()

@permission_required('IssueTracker.add_issue', login_url="/login/")
def invSpecCreate(request):
    """
    Given an inventory type in the GET, return the HTML for stage
    """
    data = request.REQUEST.copy()

    # first, figure out if inventory type exists
    inv_type = get_object_or_404(cm.InventoryType, pk=data.get('type'))

    hook = utils.issueHooks.getCreateHook(inv_type.name)

    if hook == None:
        return HttpResponseNotFound()

    return HttpResponse(hook(request))
