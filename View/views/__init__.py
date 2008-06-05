from PIL import Image

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q

import simplejson

import labtracker.settings as lset
import LabtrackerCore as core
import View
from View import models as v_models
import Machine


def dumpMachines(request, group = None):
    """
    Get's all the machines and dumps all their data out
    This will only run if Debug mode is true
    """

    if not lset.DEBUG:
        return Http404()

    args = {}

    if not group:
        args['machines'] = Machine.models.Item.objects.all()
    else:
        # fetch the group of 404
        group = get_object_or_404(Machine.models.Group, group__name=group)

        args['group'] = group.group
        args['machines'] = group.group.getItems()

    return render_to_response('View/dump_machines.html', args)

