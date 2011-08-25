from django.shortcuts import render_to_response, get_object_or_404

from Machine.models import Item, Location

def list_by_location(request, location_name):
    location = Location.objects.get(name=location_name)
    object_list = Item.objects.filter(location=location)
    return render_to_response('item_list.html', {'object_list':object_list,})
