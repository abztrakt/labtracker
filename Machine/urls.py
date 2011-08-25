from django.conf.urls.defaults import *

import Machine.hooks
import Machine.models as models

urlpatterns = patterns('',
    #url(r'^issue/create/$', 'Machine.views.issueCreate'),
    url(r'^list/(?P<location_name>\w+)/$', 'Machine.views.list_by_location'),
)

urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^detailed/(?P<object_id>\d+)/$', 'object_detail', 
        {   'queryset': models.Item.objects.all(), 
            'template_name': 'item_detailed.html' }, 
        name="Machine-detail"),
    url(r'^list/$', 'object_list', 
        {   'queryset': models.Item.objects.all(),
            'template_name': 'item_list.html' }, 
        name="Machine-list"),
)

