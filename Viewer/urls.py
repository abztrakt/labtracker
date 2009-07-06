from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'Viewer.views.index', name="viewsIndex"), 
    url(r'^dumpMachines/$', 'Viewer.views.dumpMachines', name="machine_dump"),
    url(r'^dumpMachines/(?P<group>.+)/$', 'Viewer.views.dumpMachines', name="machine_group_dump"),

# temporary url add for inventory type views
# TODO move this to admin
    url(r'^InventoryList/Type/(?P<type_id>.+)/$', 'Viewer.views.InventoryList.show_by_type', name="Viewer-InventoryList-Types"),
    url(r'^InventoryList/', 'Viewer.views.InventoryList.show_all', name="Viewer-InventoryList-All"),

# for map stuff, will need to have stuff for creating maps
# TODO move this to admin
    url(r'^MachineMap/(?P<view_name>.+)/$', 'Viewer.views.MachineMap.show',
     name="Viewer-MachineMap-view"),
    url(r'^MachineMap/(?P<view_name>.+)/edit$', 'Viewer.views.MachineMap.modify',
     name="Viewer-MachineMap-edit"),

)

