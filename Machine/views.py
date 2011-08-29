from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from Machine.models import Item, Location

def list_by_location(request, location_id):
    location = get_object_or_404(Location, ml_id=location_id)
    object_list = Item.objects.filter(location=location)
    return render_to_response('item_list.html', {'object_list':object_list,},
        context_instance=RequestContext(request))
