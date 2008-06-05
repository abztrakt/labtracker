from django.conf.urls.defaults import *

urlpatterns = patterns('',
     url(r'^dumpMachines/$', 'View.views.dumpMachines', name="machine_dump"),
     url(r'^dumpMachines/(?P<group>.+)/$', 'View.views.dumpMachines', name="machine_group_dump"),

     # for map stuff, will need to have stuff for creating maps
     # TODO move this to admin
     url(r'^modMachineMap/(?P<view_name>.+)/$', 'View.views.MachineMap.modMachineMap',
         name="machine_map_mod"),


)

