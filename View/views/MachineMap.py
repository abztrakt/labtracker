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

def machineMap(request, group_name):
    """
    Spits out a lab map
    """
    group = get_object_or_404(Machine.models.Group, group__name=group_name)
    view = get_object_or_404(View.models.View, group=group)

    data = request.GET.copy()

    if data.has_key('get_pos'):
        # in this case, we should return the positions of the machines

        items = View.models.MachineMap.objects.filter(view=view)

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

        return render_to_response('View/machineMap.html', args)

def modMachineMap(request, view_name):
    """
    Spits out map, with the machines placed on it in appropriate places
    Unmapped items, are placed in an extra panel
    """

    view = get_object_or_404(v_models.View, shortname=view_name)
    model = view.type.getModel()


    #data = request.POST.copy()
    data = request.GET.copy()

    if (data.get('save', False)):
        # need to save the computers
        unmap = data.getlist('unmap')
        map = data.getlist('map')

        # get the unmapped items
        unmap_items = v_models.MachineMap_item.objects.filter(
                item__name__in = unmap)
        if (len(unmap) != len(unmap_items)):
            print "Num requested did not match num returned"
            return HttpResponseServerError()

        unmap_items.delete()

        # get the mapped items

        # figure out which are already mapped and only need updating
        mapped_items = v_models.MachineMap_item.objects.filter(
                item__name__in = map)

        resp = { 'status': 0 }

        # for these items, update
        for item in mapped_items:
            print 'dealing with %s' % item
            xattr = "%s_x" % (item.item.name)
            yattr = "%s_y" % (item.item.name)
            sizeattr = "%s_s" % (item.item.name)
            orientattr = "%s_o" % (item.item.name)

            item.xpos = data.get(xattr, None)
            item.ypos = data.get(yattr, None)
            if None in (item.xpos, item.ypos):
                resp['error'] += "Both x and y needed: %s\n" % (item.item.name)
                return HttpResponseServerError()
                #return HttpResponse(simplejson.dumps(resp))

            param_size = data.get(sizeattr, None);
            if (param_size):
                item.size = \
                    v_models.MachineMap_Size.objects.get(name=param_size)

            orientation = data.get(orientattr, None)
            if (orientation):
                item.orientation = orientation


            item.save()


        new_names = set(map).difference(
                set([item.item.name for item in mapped_items]))

        # create new entries for each of these items
        for name in new_names:
            # first fetch the base_item
            try:
                print "Name is %s" % name
                base_item = core.models.Item.objects.get(name=name)
            except Exception, e:
                # TODO finer grained error checking
                print "Failed to get the base_item, %s" % e
                resp['error'] += "Failed to get the base_item\n"
                return HttpResponseServerError()
                #return HttpResponse(simplejson.dumps(resp))

            # with the base_item, construct new mapped_item entry
            xattr = "%s_x" % (name)
            yattr = "%s_y" % (name)
            sizeattr = "%s_s" % (name)
            orientattr = "%s_o" % (name)

            new_item = v_models.MachineMap_item(view = view, item = base_item,
                    xpos = data.get(xattr), ypos = data.get(yattr))

            size = data.get(sizeattr, None)
            if (size):
                new_item.size = \
                    v_models.MachineMap_Size.objects.get(name=size)

            new_item.orientation = data.get(orientattr, None)

            if None in (size, new_item.orientation):
                debugLog("no data on size/orientation")
                return HttpResponse(simplejson.dumps({'status': 0}))

            new_item.save()

        
        return HttpResponse(simplejson.dumps(resp))




    type = view.type.name
    map = None

    # XXX: Maybe move this to client side?
    for ext in ('png', 'jpg', 'gif'):
        try:
            path = "%s/static/img/view/%s.%s" % (lset.APP_DIR, view_name, ext)
            map = Image.open(path)
            break
        except IOError, e:
            continue

    if not map:
        return HttpResponseServerError()

    groups = view.groups.all()
    mapped_items = view.getMappedItems()
    args = {
        'groups':   groups,
        'map': {
                "ext":      ext,
                "name":     view_name,
                "width":    map.size[0],
                "height":   map.size[1]
            },
        'mapped':   mapped_items,
        'unmapped': [],
        'sizes':    v_models.MachineMap_Size.objects.all(),
        'debug':    lset.DEBUG,
    }

    # get the list of unmapped items
    mapped_set = set([m_item.item for m_item in mapped_items])

    for group in groups:
        items = group.item.all()
        args['unmapped'].extend( set(items).difference(mapped_set) )

        print args['unmapped']


    return render_to_response('View/modMachineMap.html', args)
