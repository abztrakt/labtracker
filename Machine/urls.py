from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^item/add/$', 'labtracker.Machine.admin_views.addItem'),
    (r'^item/(?P<id>\d+)/$', 'labtracker.Machine.admin_views.modItem'),
    (r'^group/add/$', 'labtracker.Machine.admin_views.addGroup'),
    (r'^group/(?P<id>\d+)/$', 'labtracker.Machine.admin_views.modGroup'),
)

