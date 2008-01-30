from django.conf.urls.defaults import *
from labtracker.IssueTracker.models import *
#import django.views.generic.list_detail
from django.views.generic.list_detail import object_list

urlpatterns = patterns('',
     url(r'^$', 'labtracker.IssueTracker.views.index', name="index"),
     (r'^search/$', 'labtracker.IssueTracker.views.search'),
     (r'^search/detailed/$', 'labtracker.IssueTracker.views.advSearch'),
     (r'^search/field/(?P<field_name>\w+)/$',
         'labtracker.IssueTracker.views.getSearchField'),
     url(r'^all/$', 'labtracker.IssueTracker.views.viewAllIssues', name='viewAll'),
     url(r'^all/(?P<page>\d+)/$', 'labtracker.IssueTracker.views.viewAllIssues', name='viewAll'),
     (r'^pref/$', 'labtracker.IssueTracker.views.user'),
     (r'^(?P<issue_id>\d+)/fetch/$', 'labtracker.IssueTracker.views.fetch'),
     url(r'^new/$', 'labtracker.IssueTracker.views.createIssue', name='createIssue'),
     (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'IssueTracker/login.html'}),
     (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'IssueTracker/logout.html'}),
     url(r'^(?P<issue_id>\d+)/$', 'labtracker.IssueTracker.views.viewIssue', name="view"),
     (r'^(?P<issue_id>\d+)/modIssue/', 'labtracker.IssueTracker.views.modIssue'),
     (r'^(?P<issue_id>\d+)/post/$', 'labtracker.IssueTracker.views.post'),
     (r'^report/(?P<report_id>\d+)/$', 'labtracker.IssueTracker.views.report'),
     (r'^report/$', 'labtracker.IssueTracker.views.reportList'),
     (r'^groups/$', 'labtracker.IssueTracker.views.getGroups'),
     (r'^items/$', 'labtracker.IssueTracker.views.getItems'),
)
