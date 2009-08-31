from django.conf.urls.defaults import *

urlpatterns = patterns('',
     url(r'^updateMachine/(?P<name>.+)/$', 
        'Tracker.views.updateMachine', name="tracker-machine"),

     url(r'^(?P<action>login|logout|ping)/(?P<macs>.+)/$', 
        'Tracker.views.track', name="track"),

     url(r'^views/available/(?P<location>.+)/$',
        'Tracker.public.openSeats', name='open-seats'),

     url(r'^views/available/$',
        'Tracker.public.openSeats', name='open-seats'),

     url(r'^views/statistics/$',
         'Tracker.stats.allStats', name='all-stats')
)
