from PIL import Image

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

import simplejson

import labtracker.settings as lset
import LabtrackerCore as core
import Viewer
from Viewer import models as v_models
from Viewer.models import MachineMap
import Machine

def show(request, group_name):
    """
    Spits out a lab map
    """
    group = get_object_or_404(Machine.models.Group, group__name=group_name)
    view = get_object_or_404(Viewer.models.Viewer, group=group)

    data = request.GET.copy()

    if data.has_key('get_pos'):
        # in this case, we should return the positions of the machines

        items = Viewer.models.MachineMap.objects.filter(view=view)

        item_info = {}

        for item in items:
            item_info[item.id] = {
                    'xpos'  : item.xpos,
                    'ypos'  : item.ypos
                }


        format = data.get('format', 'json')

        if format == "xml":
            return HttpResponseServerError()
        elif format == "json":
            return HttpResponse(simplejson.dumps(item_info))
        else:
            return HttpResponseServerError()
    else:
        args = {}
        args['group'] = group

        return render_to_response('Viewer/MachineMap/show.html', args)

@permission_required('Viewer.change_view_core', login_url="/login/")
def modify(request, view_name):
    """
    Spits out map, with the machines placed on it in appropriate places
    Unmapped items, are placed in an extra panel
    """

    # get the map
    view = MachineMap.MachineMap.objects.get(shortname=view_name)

    data = request.REQUEST.copy()

    if (data.get('save', False)):
        # need to save the computers
        unmap = data.getlist('unmap')
        map = data.getlist('map')

        unmap = [int(id) for id in unmap]
        map = [int(id) for id in map]

        # get the unmapped items
        unmap_items = MachineMap.MachineMap_Item.objects.filter(machine__pk__in = unmap)
        if (len(unmap) != len(unmap_items)):
            resp['error'] = "Could not find some of the requested items to unmap"
            return HttpResponseServerError(simplejson.dumps(resp))

        for uitem in unmap_items:
            uitem.delete()

        # figure out which are already mapped and only need updating

        # get items that are already mapped
        map_items = MachineMap.MachineMap_Item.objects.filter(machine__pk__in = map)

        resp = { 'status': 0, 'error': "" }

        def getItemInfo(id):
            return {
                'x':    data.get('map[%s][x]' % id, None),
                'y':    data.get('map[%s][y]' % id, None),
                'orient':    data.get('map[%s][orient]' % id, None),
                'size':    data.get('map[%s][size]' % id, None)
            }

        # These items already exist, so we only need to update 
        for item in map_items:
            iteminfo = getItemInfo(item.machine.pk)

            if None not in (iteminfo['x'], iteminfo['y']):
                item.xpos = iteminfo['x']
                item.ypos = iteminfo['y']

            param_size = iteminfo['size']
            if (param_size):
                item.size = \
                    MachineMap.MachineMap_Size.objects.get(name=param_size)

            orientation = iteminfo['orient']
            if (orientation):
                item.orientation = orientation

            item.save()


        # Figure out what items haven't been mapped before
        new_ids = set(map).difference(
                set([item.machine.pk for item in map_items]))

        # create new entries for each of these items
        for item_id in new_ids:
            # first fetch the base_item
            try:
                item = Machine.models.Item.objects.get(pk=item_id)
            except Exception, e:
                # TODO finer grained error checking
                resp['error'] += "Failed to get the base_item\n"
                return HttpResponseServerError(simplejson.dumps(resp))

            # with the base_item, construct new mapped_item entry
            iteminfo = getItemInfo(item_id)

            if None in (iteminfo['x'], iteminfo['y']):
                resp['error'] += "Both x and y needed: %s\n" % (item.pk)
                return HttpResponseServerError(simplejson.dumps(resp))

            new_item = MachineMap.MachineMap_Item(view = view, machine = item,
                    xpos = iteminfo['x'], ypos = iteminfo['y'])

            size = iteminfo['size']
            if (size):
                new_item.size = \
                    MachineMap.MachineMap_Size.objects.get(name=size)


            new_item.orientation = iteminfo['orient']

            if None in (size, new_item.orientation):
                return HttpResponse(simplejson.dumps({'status': 0}))

            new_item.save()

        
        return HttpResponse(simplejson.dumps(resp))


    map = None

    # XXX: Maybe move this to client side?
    for ext in ('png', 'jpg', 'gif'):
        try:
            path = "%s/static/img/Viewer/%s.%s" % (lset.APP_DIR, view_name, ext)
            map = Image.open(path)
            break
        except IOError, e:
            continue

    if not map:
        resp['error'] = "Couldn't find map to load"
        return HttpResponseServerError(simplejson.dumps(resp))

    groups = view.groups.all()
    map_items = view.getMappedItems()
    args = {
        'groups':   groups,
        'map': {
                "ext":      ext,
                "name":     view_name,
                "width":    map.size[0],
                "height":   map.size[1]
            },
        'mapped':   map_items,
        'unmapped': view.getUnmappedItems(),
        'sizes':    MachineMap.MachineMap_Size.objects.all(),
        'debug':    lset.DEBUG,
    }

    return render_to_response('Viewer/MachineMap/modify.html', args,
            context_instance=RequestContext(request))
