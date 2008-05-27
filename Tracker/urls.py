from django.conf.urls.defaults import *

urlpatterns = patterns('',
     url(r'^updateMachine/(?P<name>.+)/$', 
        'Tracker.views.updateMachine', name="machine_update"),
)
