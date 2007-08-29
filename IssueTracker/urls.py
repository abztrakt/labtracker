from django.conf.urls.defaults import *
from labtracker.IssueTracker.models import *


urlpatterns = patterns('',
    # Example:
    # (r'^labtracker/', include('labtracker.foo.urls')),

    # Uncomment this for admin:
     (r'^$', 'labtracker.IssueTracker.views.index'),
     #(r'^all/$', 'labtracker.IssueTracker.views.allIssues'),
     (r'^all/$', 'django.views.generic.list_detail.object_list', 
         {'queryset': Issue.objects.all().order_by('-last_modified'),}),
     (r'^pref/$', 'labtracker.IssueTracker.views.user'),
     url(r'^new/$', 'labtracker.IssueTracker.views.create', name='create'),
     (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'IssueTracker/login.html'}),
     (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'IssueTracker/logout.html'}),
     url(r'^(?P<issue_id>\d+)/$', 'labtracker.IssueTracker.views.view', name="view"),
     (r'^(?P<issue_id>\d+)/post/$', 'labtracker.IssueTracker.views.post'),
     (r'^report/(?P<report_id>\d+)/$', 'labtracker.IssueTracker.views.report'),
     (r'^report/$', 'labtracker.IssueTracker.views.reportList'),
)
