import time
import datetime
from PIL import Image

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
from django.db.models import Q

def info(request, view_name):
    
    available_items = None
    ret_data = {}
    if request.method == 'GET':
        view = get_object_or_404(v_models.MachineMap, shortname=view_name)
         
        available_items = view.getMappedItems().exclude(machine__item__status__name__contains='Inuse').exclude(machine__item__unusable=True)
        available_count = available_items.count()
        windows7_count = available_items.filter(machine__item__type__platform__name='Windows 7').count()
        winxp_count = available_items.filter(machine__item__type__platform__name='Windows XP').count()
        osX_count = available_items.filter(
            Q(machine__item__type__platform__name='Mac OS X') | Q(machine__item__type__platform__name='MAC OSX')
        ).count()
        total_count = view.getMappedItems().count()
        ret_data['available_machines'] =available_count
        ret_data['total_machines'] = total_count
        ret_data['available_win7'] = windows7_count
        ret_data['available_winxp'] = winxp_count
        ret_data['available_mac'] = osX_count
        return HttpResponse(simplejson.dumps(ret_data))
    else:
        ret_data['error']= "No understandable request made." 
        return HttpResponseServerError(simplejson.dumps(ret_data))


def getMapInfo(view_name):
    map = None

    for ext in ('png', 'jpg', 'gif'):
        try:
            path = "%s/static/img/Viewer/%s.%s" % (lset.APP_DIR, view_name, ext)
            map = Image.open(path)
            break
        except IOError, e:
            continue

    return map

def show(request, view_name):
    """
    Spits out a lab map
    """
    view = get_object_or_404(v_models.MachineMap, shortname=view_name)

    def getUnmappedData():
        items = view.getUnmappedItems()
        ret_data ={}
        for item in items:
            data = {}
            data['name'] = item.name
            ret_data[item.pk] = data
        return ret_data

    def getJSONData(last=None):
        """
        PRE: Takes a datetime object and will gets machines added after that date
        POST: Returns machine information in JSON format
        """
        items = view.getMappedItems().exclude(last_modified__lte=last, machine__item__last_modified__lte=last)
        ret_data = {}
        for item in items:
            data = {}
            machine_info = False
            mapped_info = False
            if last:
                if item.date_added > last:
                    # gotta get it all
                    mapped_info = True
                    machine_info = True
                else:
                    mapped_info = item.last_modified > last
                    machine_info = item.machine.item.last_modified > last
            else:
                machine_info = True
                mapped_info = True

            if machine_info:
                states = [a for (a,) in item.machine.item.status.values_list('name')]
                unusable = item.machine.item.unusable
                if 'Inuse' in states:
                    data['state'] = 'occupied'
                elif not unusable:
                    data['state']= 'usable'
                else:
                    data['state'] = 'unusable'


            if mapped_info:
                data['x'] = item.xpos
                data['y'] = item.ypos
                data['orient'] = item.orientation
                data['size'] = item.size.name

            if data:
                data['name'] = item.machine.name,
                broken = False
                verified = False
                if item.machine.unresolved_issues():
                    broken=True
                if item.machine.item.verified:
                    verified=True
                if item.orientation == 'H':
                    width = 10+item.size.height
                else:
                    width = 10 + item.size.width
                data['verified'] = verified
                data['broken'] = broken
                # .type is a python thing 
                #import pdb; pdb.set_trace()
                data['type'] = item.machine.item.type.name 
                data['mac1'] = item.machine.item.mac1
                data['mac2'] = item.machine.item.mac2
                data['ip'] = item.machine.item.ip
                data['wall_port'] = item.machine.item.wall_port
                data['uw_tag'] = item.machine.item.uw_tag
                data['manu'] = item.machine.item.manu_tag
                data['width'] = width 
                ret_data[item.machine.pk] = data

        
        return ret_data
    if request.is_ajax():
        """
        A request is being made on data
        """
        data = request.GET.copy()
        ret = {}
        last = data.get('last', None)
        if last:
            try:
                last = float(last)
                last = datetime.datetime.fromtimestamp(last)
            except Exception, e:
                last = None

        try:
            ret['machines'] = getJSONData(last)
            ret['deletemachines'] = getUnmappedData()
        except Exception, e:
            ret['error'] = "No understandable request made."
            return HttpResponseServerError(simplejson.dumps(ret))

        ret['time'] = time.mktime(time.localtime())

        return HttpResponse(simplejson.dumps(ret))

    # if we are down here, we are just rendering the map
    staff = request.user.is_staff
    map = getMapInfo(view_name)

    if not map:
        return HttpResponseServerError("Couldn't find map to load")

    
    map_items = []
   
    for item in view.getMappedItems():
        states = [a for (a,) in item.machine.item.status.values_list('name')]
        unresolved = item.machine.item.unresolved_issues()
        broken = None
        verified = None
        list_pos = None
        if staff:
            if item.machine.item.verified:
                verified = 'verified' 
            if unresolved.count() != 0:
                broken = 'broken'
            else:
                broken = 'not_broken'
            if item.orientation == 'H':
                list_pos = item.xpos + item.size.height + 10
            else:
                list_pos = item.xpos + item.size.width+ 10
        if item.machine.item.unusable:
            status = 'unusable'
        elif 'Inuse' in states:
            status = 'occupied'
        else:
            status = 'usable'
        item_dict = {
                'machine': item.machine,
                'size': item.size,
                'orientation': item.orientation,
                'ypos': item.ypos,
                'xpos': item.xpos,
                'status':status,
                'broken':broken,
                'verified': verified,
                'name': item.machine.item.name,
                'wall_port': item.machine.item.wall_port,
                'mac1': item.machine.item.mac1,
                'mac2': item.machine.item.mac2,
                'ip': item.machine.item.ip,
                'uw_tag': item.machine.item.uw_tag,
                'type': item.machine.item.type.name,
                'manu_tag': item.machine.item.manu_tag,
                'list_pos': list_pos,
            }
        map_items.append(item_dict)

    groups = view.groups.all()

    args = {
        'show':     True,
        'staff':    staff,
        'view':     view,
        'mapped':   map_items,
        'sizes':    v_models.MachineMap_Size.objects.all(),
        'status':   ['usable','unusable','occupied'],
        'map_url':  map.filename.replace(settings.APP_DIR, ""),
        'map': {
                "name":     view_name,
                "width":    map.size[0],
                "height":   map.size[1]
                },
            'debug' :   lset.DEBUG,
            }
    return render_to_response('Viewer/MachineMap/show.html', args,
            context_instance=RequestContext(request))

@permission_required('Viewer.change_viewcore', login_url="/login/")
def modify(request, view_name):
    """
    Spits out map, with the machines placed on it in appropriate places
    Unmapped items, are placed in an extra panel
    """

    # get the map
    view = v_models.MachineMap.objects.get(shortname=view_name)

    data = request.REQUEST.copy()

    if (data.get('save', False)):
        # need to save the computers
        resp = { 'status': 0, 'error': "" }
        unmap = data.getlist('unmap[]')
        map = data.getlist('map[]')

        unmap = [int(id) for id in unmap]
        map = [int(id) for id in map]

        # get the unmapped items
        unmap_items = v_models.MachineMap_Item.objects.filter(view = view, 
                machine__pk__in = unmap)
        if (len(unmap) != len(unmap_items)):
            resp['error'] = "Could not find some of the requested items to unmap"
            return HttpResponseServerError(simplejson.dumps(resp))

        for uitem in unmap_items:
            uitem.delete()

        # figure out which are already mapped and only need updating

        # get items that are already mapped
        map_items = v_models.MachineMap_Item.objects.filter(view = view, 
                machine__pk__in = map)

        

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
                    v_models.MachineMap_Size.objects.get(name=param_size)

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

            new_item = v_models.MachineMap_Item(view = view, machine = item,
                    xpos = iteminfo['x'], ypos = iteminfo['y'])

            size = iteminfo['size']
            if (size):
                new_item.size = \
                    v_models.MachineMap_Size.objects.get(name=size)


            new_item.orientation = iteminfo['orient']

            if None in (size, new_item.orientation):
                return HttpResponse(simplejson.dumps({'status': 0}))

            new_item.save()

        
        return HttpResponse(simplejson.dumps(resp))

    map = getMapInfo(view_name)

    if not map:
        return HttpResponseServerError("Couldn't find map to load")
    
    groups = view.groups.all()
    map_items = view.getMappedItems()



    args = {
        'groups':   groups,
        'map_url':  map.filename.replace(settings.APP_DIR, ""),
        'map': {
                "name":     view_name,
                "width":    map.size[0],
                "height":   map.size[1]
            },
        'view':     view,
        'mapped':   map_items,
        'unmapped': view.getUnmappedItems(),
        'sizes':    v_models.MachineMap_Size.objects.all(),
        'debug':    lset.DEBUG,
    }

    return render_to_response('Viewer/MachineMap/modify.html', args,
            context_instance=RequestContext(request))
