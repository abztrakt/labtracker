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

def get_item_list(getattr, getparam,  orderby):
    if getattr:
        items = core.models.Item.objects.get(getattr + "=" + getparam).order_by(orderby)
    else:
        items = core.models.Item.objects.all().order_by(orderby)

    item_list = []

    for item in items:
        item_dict = {
                'item_id': item.item_id,
                'name': item.name,
                'type': item.it.name,
                'group_id': item.group_set.values()[0]['group_id'],
                'group': item.group_set.values()[0]['name']
        }

        item_list.append(item_dict)

    return item_list

def show_all(request):
    item_list = get_item_list('', '', 'item_id')
    return render_to_response('InventoryList/show_all.html', {'item_list': item_list}, context_instance=RequestContext(request))

def show_by_group(request, group_id):
    if group_id:
        #item_list = get_item_list('group_set', group_id, 'item_name') #WILL NOT WORK!
        return render_to_response()
    else: 
        groups = core.models.Group.objects.all().order_by('name')
        return render_to_response('InventoryList/show_by_group.html', {'groups_list': groups}, context_instance=RequestContext(request))

def show_by_type(request, type_id):
    if type_id:
        it = core.models.InventoryType.objects.get(pk=type_id)
        item_list = get_item_list('it', str(it.inv_id), 'item_id')
        return render_to_response('InventoryList/show_by_type.html', {'item_list': item_list}, context_instance=RequestContext(request))
    else:
        inventory_types = core.models.InventoryType.objects.all().order_by('name')
        return render_to_response('InventoryList/show_by_type.html', {'inventory_list': inventory_types}, context_instance=RequestContext(request))

