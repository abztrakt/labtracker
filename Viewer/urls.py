from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'Viewer.views.index', name="viewIndex"), 
    url(r'^dumpMachines/$', 'Viewer.views.dumpMachines', name="machine_dump"),
    url(r'^dumpMachines/(?P<group>.+)/$', 'Viewer.views.dumpMachines', name="machine_group_dump"),

# for map stuff, will need to have stuff for creating maps
# TODO move this to admin
    url(r'^MachineMap/(?P<view_name>.+)/$', 'Viewer.views.MachineMap.show',
     name="machine_map_show"),
    url(r'^MachineMap/(?P<view_name>.+)/modify$', 'Viewer.views.MachineMap.modify',
     name="machine_map_mod"),

)

