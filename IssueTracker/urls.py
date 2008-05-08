from django.conf.urls.defaults import *

urlpatterns = patterns('',
     url(r'^$', 'IssueTracker.views.index', name="index"),
     (r'^checkuser/(?P<name>\w+)/$', 'IssueTracker.views.ajax.userCheck'),
     (r'^search/$', 'IssueTracker.views.search'),
     (r'^search/detailed/$', 'IssueTracker.views.advSearch'),
     (r'^search/field/(?P<field_name>\w+)/$',
         'IssueTracker.views.ajax.getSearchField'),
     url(r'^all/$', 'IssueTracker.views.viewAllIssues', name='viewAll'),
     url(r'^all/(?P<page>\d+)/$', 'IssueTracker.views.viewAllIssues', name='viewAll'),
     (r'^(?P<issue_id>\d+)/fetch/$', 'IssueTracker.views.fetch'),
     url(r'^new/$', 'IssueTracker.views.createIssue', name='createIssue'),

     url(r'^(?P<issue_id>\d+)/$', 'IssueTracker.views.viewIssue', name="view"),
     (r'^(?P<issue_id>\d+)/modIssue/', 'IssueTracker.views.modIssue'),
     (r'^(?P<issue_id>\d+)/post/$', 'IssueTracker.views.post'),
     (r'^report/(?P<report_id>\d+)/$', 'IssueTracker.views.report'),
     (r'^report/$', 'IssueTracker.views.reportList'),
     (r'^groups/$', 'IssueTracker.views.ajax.getGroups'),
     (r'^items/$', 'IssueTracker.views.ajax.getItems'),
)
