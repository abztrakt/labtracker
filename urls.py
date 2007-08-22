from django.conf.urls.defaults import *
from django.contrib import databrowse
from labtracker.Machine.models import *
#from labtracker.LabtrackerCore.models import *

#databrowse.site.register(labtracker.Machine.model.Machine)
#databrowse.site.register(Item)
databrowse.site.register(Machine)

urlpatterns = patterns('',
    # Example:
    # (r'^labtracker/', include('labtracker.foo.urls')),

    # Uncomment this for admin:
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '/var/www/django_apps/labtracker/static/css/', 'show_indexes': True}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '/var/www/django_apps/labtracker/static/js/', 'show_indexes': True}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '/var/www/django_apps/labtracker/static/', 'show_indexes': True}),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^$', include('labtracker.IssueTracker.urls')),
    (r'^issue/', include('labtracker.IssueTracker.urls')),
)
