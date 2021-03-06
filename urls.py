from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

#from labtracker.admin import default_admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'LabtrackerCore.views.dashboard'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '%s/static/' % (settings.APP_DIR), 'show_indexes': True}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Auth related items
    url(r'^login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', 
        {'template_name': 'logout.html'}, name='logout'),

    (r'^pref/', include('LabtrackerCore.urls')),
    (r'^issue/', include('IssueTracker.urls')),


    (r'^views/', include('Viewer.urls')),
    (r'^tracker/', include('labtracker.Tracker.urls')),

    (r'^machine/', include('Machine.urls')),
)
