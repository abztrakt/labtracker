from PIL import Image

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.template import RequestContext

import simplejson

import labtracker.settings as lset
import LabtrackerCore as core
import Viewer
from Viewer import models as v_models
import Machine


def dumpMachines(request, group = None):
    """
    Get's all the machines and dumps all their data out
    This will only run if Debug mode is true
    """

    if not lset.DEBUG:
        return HttpResponseForbidden()

    args = {}

    if not group:
        args['machines'] = Machine.models.Item.objects.all()
    else:
        # fetch the group of 404
        group = get_object_or_404(Machine.models.Group, group__name=group)

        args['group'] = group.group
        args['machines'] = group.group.getItems()

    return render_to_response('Viewer/dump_machines.html', args)

@permission_required('Viewer.can_view', login_url="/login/")
def index(request):
    """
    Grab all available views and list them out
    """

    view_types = v_models.ViewType.objects.all()
    views = []
    for type in view_types:
        # convert all fetched views to the child view
        view_list = [ v.get_child()
                for v in v_models.ViewCore.objects.filter(
                type=v_models.ViewType.objects.get(name=type.name))]
        views.append(( type.name, view_list ))

    return render_to_response('Viewer/index.html', 
            {'views': views }, context_instance=RequestContext(request))

