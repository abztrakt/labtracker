from django.conf.urls.defaults import *

urlpatterns = patterns('IssueTracker.views',
     url(r'^$', 'index', name="issueIndex"),
     url(r'^all/$', 'allUnresolved', name='viewAll'),
     url(r'^all/(?P<page>\d+)/$', 'allUnresolved', name='viewAll'),
     (r'^(?P<issue_id>\d+)/fetch/$', 'fetch'),
     url(r'^new/$', 'createIssue', name='createIssue'),

     url(r'^(?P<issue_id>\d+)/$', 'viewIssue', name="view"),
     url(r'^(?P<issue_id>\d+)/post/$', 'post', name='IssueTracker-addComment'),
     url(r'^(?P<issue_id>\d+)/modIssue/', 'modIssue', name='IssueTracker-modIssue'),

     (r'^report/(?P<report_id>\d+)/$', 'report'),
     (r'^report/$', 'reportList'),
)

urlpatterns += patterns('IssueTracker.views.search',
     url(r'^search/$', 'search', name="issueSearch"),
     (r'^search/detailed/$', 'advSearch'),
)

urlpatterns += patterns('IssueTracker.views.ajax',
     (r'^checkuser/(?P<name>\w+)/$', 'userCheck'),

     (r'^search/field/(?P<field_name>\w+)/$', 'getSearchField'),

     (r'^groups/$', 'getGroups'),
     (r'^items/$', 'getItems'),
)
