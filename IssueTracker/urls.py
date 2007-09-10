from django.conf.urls.defaults import *
from labtracker.IssueTracker.models import *
#import django.views.generic.list_detail
from django.views.generic.list_detail import object_list

urlpatterns = patterns('',
    # Example:
    # (r'^labtracker/', include('labtracker.foo.urls')),

    # Uncomment this for admin:
     url(r'^$', 'labtracker.IssueTracker.views.index', name="index"),
     (r'^search/$', 'labtracker.IssueTracker.views.search'),
     url(r'^all/$', object_list, 
         {'queryset': Issue.objects.all().order_by('-last_modified'),}, 
         name='all'),
     (r'^pref/$', 'labtracker.IssueTracker.views.user'),
     url(r'^new/$', 'labtracker.IssueTracker.views.createIssue', name='createIssue'),
     (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'IssueTracker/login.html'}),
     (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'IssueTracker/logout.html'}),
     url(r'^(?P<issue_id>\d+)/$', 'labtracker.IssueTracker.views.view', name="view"),
     (r'^(?P<issue_id>\d+)/modIssue/', 'labtracker.IssueTracker.views.modIssue'),
     (r'^(?P<issue_id>\d+)/post/$', 'labtracker.IssueTracker.views.post'),
     (r'^report/(?P<report_id>\d+)/$', 'labtracker.IssueTracker.views.report'),
     (r'^report/$', 'labtracker.IssueTracker.views.reportList'),
     (r'^groups/(?P<it_type>\d+)/$', 'labtracker.IssueTracker.views.getGroups'),
     (r'^items/(?P<group_id>\d+)/$', 'labtracker.IssueTracker.views.getItems'),
)
