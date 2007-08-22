from django.conf.urls.defaults import *


urlpatterns = patterns('',
    # Example:
    # (r'^labtracker/', include('labtracker.foo.urls')),

    # Uncomment this for admin:
     (r'^$', 'labtracker.IssueTracker.views.index'),
     (r'^pref/$', 'labtracker.IssueTracker.views.user'),
     (r'^new/$', 'labtracker.IssueTracker.views.create'),
     (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'IssueTracker/login.html'}),
     (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'IssueTracker/logout.html'}),
     (r'^(?P<issue_id>\d+)/$', 'labtracker.IssueTracker.views.view'),
     #(r'^(?P<issue_id>\d+)/post/$', 'labtracker.IssueTracker.views.post'),
     (r'^all/$', 'labtracker.IssueTracker.views.allIssues'),
     (r'^report/(?P<report_id>\d+)/$', 'labtracker.IssueTracker.views.report'),
     (r'^report/$', 'labtracker.IssueTracker.views.reportList'),
)
