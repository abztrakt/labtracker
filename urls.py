from django.conf.urls.defaults import *
import labtracker.settings as lset

app_dir = lset.APP_DIR


urlpatterns = patterns('',
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': "%s/static/css/" % (app_dir), 'show_indexes': True}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': "%s/static/js/" % (app_dir), 'show_indexes': True}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '/var/www/django_apps/labtracker/static/', 'show_indexes': True}),

    (r'^admin/', include('django.contrib.admin.urls')),

    #(r'^databrowse/(.*)', databrowse.site.root),
    #(r'^$', include('labtracker.IssueTracker.urls')),
    (r'^issue/', include('labtracker.IssueTracker.urls')),
)
