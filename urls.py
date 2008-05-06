from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': "%s/static/css/" % (settings.APP_DIR), 'show_indexes': True}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': "%s/static/js/" % (settings.APP_DIR), 'show_indexes': True}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '/var/www/django_apps/labtracker/static/', 'show_indexes': True}),

    (r'^admin/', include('django.contrib.admin.urls')),

    #(r'^databrowse/(.*)', databrowse.site.root),
    (r'^issue/', include('IssueTracker.urls')),
)
