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
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^databrowse/(.*)', databrowse.site.root),
     (r'^issue/', include('labtracker.IssueTracker.urls')),
)
