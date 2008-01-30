from django.conf.urls.defaults import *
from django.contrib import databrowse
import labtracker.Machine.models as machine

import django.core.management as dman
import labtracker.settings as lset
import django.core.management.commands.startapp as startapp

app_dir = dman.setup_environ(lset)              # get app_dir from settings


urlpatterns = patterns('',
    # Example:
    # (r'^labtracker/', include('labtracker.foo.urls')),

    # Uncomment this for admin:
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': "%s/static/css/" % (app_dir), 'show_indexes': True}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': "%s/static/js/" % (app_dir), 'show_indexes': True}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '/var/www/django_apps/labtracker/static/', 'show_indexes': True}),
    # (r'^admin/Machine/group/add/$', 'labtracker.Machine.admin_views.addGroup'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^databrowse/(.*)', databrowse.site.root),
    #(r'^$', include('labtracker.IssueTracker.urls')),
    (r'^issue/', include('labtracker.IssueTracker.urls')),
)
