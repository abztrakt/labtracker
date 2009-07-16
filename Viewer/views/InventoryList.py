import time
import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

import simplejson

import labtracker.settings as lset
import LabtrackerCore as core
import Viewer
from Viewer import models as v_models
#from Viewer.models import MachineMap
import Machine

def show_all(request, group_id, it_id):
    # Filter to include both group and inventory type, incorporate later
    group_id = int(group_id)
    it_id = int(it_id)
    if (group_id == 0)  and (it_id == 0):
        items = core.models.Item.objects.all()
    elif it_id == 0:
        items = core.models.Item.objects.filter(it=it_id)
    elif group_id == 0:
        items = core.models.Item.objects.filter(it=it_id)
    else:
        items = core.models.Item.objects.filter(it=it_id)
    
    items = core.utils.generateOrderingArgs(request, items)
    item_list = []

    for item in items['objects']:
        item_dict = {
                'item_id': item.item_id,
                'name': item.name,
                'type': item.it.name,
                'group_id': item.group_set.values()[0]['group_id'],
                'group': item.group_set.values()[0]['name']
        }
        item_list.append(item_dict)

    args = {'item_list': item_list, 'category': ''}
    
    #item_list = get_item_list(request, '', '', 'item_id')
    return render_to_response("InventoryList/show_all.html", args, context_instance=RequestContext(request))

def show_filter(request):
    """
    Displays a list of inventory types and groups to sort items by.
    """

    # Create a 2-dimensional table, with Groups as rows and iType as columns
    it = core.models.InventoryType.objects.all()
    groups = core.models.Group.objects.all()

    args = {}
    
    # VERY expensive operation O(n^2). Can be made faster?
    rows = []
    #Rows
    for types in it:
        columns = []
        #Columns
        for group in groups:
            cell = {
                'inv_id': types.inv_id,
                'group_id': group.group_id
            }
            columns.append(cell)
        rows.append(columns)

    args['table'] = rows

    return render_to_response("InventoryList/show_filter.html", args, context_instance=RequestContext(request))
