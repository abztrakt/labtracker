from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'Viewer.views.index', name="viewsIndex"), 
    url(r'^dumpMachines/$', 'Viewer.views.dumpMachines', name="machine_dump"),
    url(r'^dumpMachines/(?P<group>.+)/$', 'Viewer.views.dumpMachines', name="machine_group_dump"),

# temporary url add for inventory type views
# TODO move this to admin
    url(r'^InventoryList/$', 'Viewer.views.InventoryList.show_filter', name="Viewer-InventoryList-All"),
    url(r'^InventoryList/(\d+)/(\d+)/$', 'Viewer.views.InventoryList.show_all', name="Viewer-InventoryList-Items"),

# for map stuff, will need to have stuff for creating maps
# TODO move this to admin
    url(r'^MachineMap/(?P<view_name>.+)/$', 'Viewer.views.MachineMap.show',
     name="Viewer-MachineMap-view"),
    url(r'^MachineMap/(?P<view_name>.+)/edit$', 'Viewer.views.MachineMap.modify',
     name="Viewer-MachineMap-edit"),

)

