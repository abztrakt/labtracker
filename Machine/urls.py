from django.conf.urls.defaults import *

import Machine.hooks
import Machine.models as models

urlpatterns = patterns('',
    #url(r'^issue/create/$', 'Machine.views.issueCreate'),
)

urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^detailed/(?P<object_id>\d+)/$', 'object_detail', 
        {   'queryset': models.Item.objects.all(), 
            'template_name': 'item_detailed.html' }, 
        name="Machine-detail"),
)

