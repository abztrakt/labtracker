from django import forms
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

def createItemList(items, field='Item'):
    list = {}

    for item in items:
        data = forms.models.model_to_dict(item.item)
        data['name'] = item.name
        list[item.item.item_id] = data

    return list

def generateList(request, data, qdict, page):
    """
    Generates a list of issues
    Take some arguments from user in data, the page number to show and the returned query
    items, render out to user
    """

    # TODO need user-defined limits
    num_per_page = data.get('numperpage', 30)

    last_order_by = data.get('orderby', 'last_modified')
    last_order_method = data.get('ometh', 'ASC')


    if last_order_by == 'id':
        order_by = 'issue_id'
    else:
        order_by = last_order_by

    if last_order_method == "ASC":
        order_method = ''
    else:
        order_method = '-'

    # FIXME this isn't working, how ridiculous
    issues = qdict.order_by(order_method + order_by)[(page - 1) * 30:page * 30]
    #issues = qdict[(page - 1) * 30:page * 30] #lambda a, b: cmp(getattr(a, order_by), getattr(b, order_by) ))

    args = {
        'issueList': issues,
        'last_order_method' : last_order_method,
        'order' : order_by,
        'search_term':  data.get('search_term', False)
    }

    args['cols'] = {
            'id'            : { 'class': 'r_issue_id', 'order': 'ASC' },
            'title'         : { 'class': 'r_title', 'order': 'ASC' },
            'item'          : { 'class': 'r_item', 'order': 'ASC' },
            'it'            : { 'class': 'r_inv_t', 'order': 'ASC' },
            'group'         : { 'class': 'r_group', 'order': 'ASC' },
            'reporter'      : { 'class': 'r_reporter', 'order': 'ASC' },
            'assignee'      : { 'class': 'r_assignee', 'order': 'ASC' },
            'post_time'     : { 'class': 'r_post_time', 'order': 'ASC' },
            'last_modified' : { 'class': 'r_last_modified', 'order': 'ASC' },
        }

    if args['cols'][last_order_by]['order'] == last_order_method:
        if last_order_method == "ASC":
            args['cols'][last_order_by]['order'] = "DESC"
        else:
            args['cols'][last_order_by]['order'] = "ASC"

    if args['search_term']:
        # kludgy way of doing things
        args['extraArgs'] = '&search_term=%s' % ( args['search_term'] )


    # FIXME should not be rendering here
    return render_to_response("IssueTracker/issue_list.html", args,
            context_instance=RequestContext(request))

