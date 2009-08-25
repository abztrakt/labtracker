from datetime import datetime
from md5 import md5

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils
import Tracker.models as t_models

def openSeats(request, location=None):
    """
    Count and list all current open seats in the given location
    """
    items_all = m_models.Item.objects.all()
    stats = t_models.Statistics.objects.all()
    locations_all = m_models.Location.objects.all()
    args = {}

    if location:
        place = locations_all.get(pk=location)
        items_all = items_all.filter(location=place)

        total = items_all.count()
        open = total

        items_list = []

        for item in items_all:

            available = True

            # Inefficient, but we have a fairly small data set.
            for status in item.status.values():
                if status['name'] == 'Inuse':
                    available = False
                    open = open - 1
                    break

            items_dict = {
                    'name': item.name,
                    'item_id': item.item_id,
                    'location': place.name,
                    'location_id': place.ml_id,
                    'building': place.building,
                    'floor': place.floor,
                    'room': place.room,
                    'available': available,
            }
            items_list.append(items_dict)

        args['items_list'] = items_list
        args['place'] = place
        args['open'] = open
        args['total'] = total

        return render_to_response('place.html', args, context_instance=RequestContext(request))
    else:
        # Give list of all locations, availability, and statistics for each location
        locations_all = m_models.Location.objects.all()
        location_list = []

        for place in locations_all:
            items = items_all.filter(location=place)
            total = items.count() 
            open = total

            # VERY INEFFICIENT! Runs in O(n^3) time with potentially large data sets. Can this be made faster?
            for item in items:
                for status in item.status.values():
                    if status['name'] == 'Inuse':
                        open = open - 1
                        break

            location_dict = {
                    'id': place.ml_id,
                    'location': place.name,
                    'building': place.building,
                    'total': total,
                    'open': open
            }
            location_list.append(location_dict)

        args['location_list'] = location_list

        return render_to_response('locations.html', args, context_instance=RequestContext(request))
