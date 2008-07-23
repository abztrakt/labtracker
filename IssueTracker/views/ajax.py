from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404

import simplejson

import IssueTracker.search as issueSearch
import LabtrackerCore.models as LabtrackerCore
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
        resp['exists'] = 1
        resp['id'] = user.id
        resp['active'] = user.is_active
        resp['username'] = user.username
        resp['email'] = user.email
    except ObjectDoesNotExist, e:
        resp['exists'] = 0

    return HttpResponse(simplejson.dumps(resp))


@permission_required('IssueTracker.add_issue')
def getItems(request):
    """
    Given an inventory type, will return a list of groups that belongs to that
    inventory_type
    """

    if request.method == "POST":
        data = request.POST.copy()
    elif request.method == "GET":
        data = request.GET.copy()

    if not data.has_key('group_id'):
        group_ids = []
    else:
        group_ids = data.getlist('group_id')

    items = {}
    # fetch the groups
    if len(group_ids) == 0 or "" in group_ids:
        # fetch all groups
        items = utils.createItemList(LabtrackerCore.Item.objects.order_by('it'))
    else:
        groups = LabtrackerCore.Group.objects.in_bulk(group_ids).values()

        # for each group, get all the items
        for group in groups:
            items.update(utils.createItemList(group.items.all()))

    # get the items in the group
    type = data.get("type", "json")
    
    if type == "xml":
        # TODO XML serialization
        pass
    else:
        return HttpResponse(simplejson.dumps(items))

@permission_required('IssueTracker.add_issue')
def getGroups(request):
    """
    Given an inventory type, will return a list of groups that belongs to that
    inventory_type
    """
    if request.method == "POST":
        data = request.POST.copy()
    elif request.method == "GET":
        data = request.GET.copy()

    if not data.has_key('it_id'):
        it_types = []
    else:
        it_types = data.getlist('it_id')
    
    groups = []
    if len(it_types) == 0 or "" in it_types:
        # get all groups
        groups = utils.createGroupList(LabtrackerCore.InventoryType.objects.all())
    else:
        groups = utils.createGroupList(LabtrackerCore.InventoryType.objects.in_bulk(it_types).values())

    type = data.get("type", "json")
    
    if type == "xml":
        # TODO XML serialization
        pass
    else:
        return HttpResponse(simplejson.dumps(groups))
