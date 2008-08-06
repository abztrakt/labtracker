from django.conf.urls.defaults import *
from django.conf import settings

from labtracker.admin import default_admin

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '%s/static/' % (settings.APP_DIR), 'show_indexes': True}),

    (r'^admin/(.*)', default_admin.root),
    #(r'^databrowse/(.*)', databrowse.site.root),

    # Auth related items
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, 
        name='logout'),

    (r'^pref/', include('LabtrackerCore.urls')),
    (r'^issue/', include('IssueTracker.urls')),


    (r'^views/', include('Viewer.urls')),
    (r'^tracker/', include('labtracker.Tracker.urls')),
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/issue/'}),

    url(r'^feeds/latest/(?P<assignee>.*)/$', 'labtracker.feeds.issuesByAssignee', name='issuesByAssignee'), 
    url(r'^feeds/issues/$', 'labtracker.feeds.issuesAll', name='issuesAll'), 
)
