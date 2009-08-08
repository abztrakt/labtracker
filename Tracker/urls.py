from django.conf.urls.defaults import *

urlpatterns = patterns('',
     url(r'^updateMachine/(?P<name>.+)/$', 
        'Tracker.views.updateMachine', name="tracker-machine"),

     url(r'^Tracker/(?P<action>login|logout|ping)/(?P<macs>.+)/$', 
        'Tracker.views.track', name="track"),
)
