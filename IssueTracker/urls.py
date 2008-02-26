from django.conf.urls.defaults import *
from labtracker.IssueTracker.models import *
#import django.views.generic.list_detail
from django.views.generic.list_detail import object_list

urlpatterns = patterns('',
     url(r'^$', 'IssueTracker.views.index', name="index"),
     (r'^checkuser/(?P<name>\w+)/$', 'IssueTracker.views.userCheck'),
     (r'^search/$', 'IssueTracker.views.search'),
     (r'^search/detailed/$', 'IssueTracker.views.advSearch'),
     (r'^search/field/(?P<field_name>\w+)/$',
         'IssueTracker.views.getSearchField'),
     url(r'^all/$', 'IssueTracker.views.viewAllIssues', name='viewAll'),
     url(r'^all/(?P<page>\d+)/$', 'IssueTracker.views.viewAllIssues', name='viewAll'),
     (r'^pref/$', 'IssueTracker.views.user'),
     (r'^(?P<issue_id>\d+)/fetch/$', 'IssueTracker.views.fetch'),
     url(r'^new/$', 'IssueTracker.views.createIssue', name='createIssue'),
     (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'IssueTracker/login.html'}),
     (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'IssueTracker/logout.html'}),
     url(r'^(?P<issue_id>\d+)/$', 'IssueTracker.views.viewIssue', name="view"),
     (r'^(?P<issue_id>\d+)/modIssue/', 'IssueTracker.views.modIssue'),
     (r'^(?P<issue_id>\d+)/post/$', 'IssueTracker.views.post'),
     (r'^report/(?P<report_id>\d+)/$', 'IssueTracker.views.report'),
     (r'^report/$', 'IssueTracker.views.reportList'),
     (r'^groups/$', 'IssueTracker.views.getGroups'),
     (r'^items/$', 'IssueTracker.views.getItems'),
)
