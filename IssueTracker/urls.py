from django.conf.urls.defaults import *

urlpatterns = patterns('IssueTracker.views',
     (r'^(?P<issue_id>\d+)/fetch/$', 'fetch'),
     url(r'^new/$', 'createIssue', name='createIssue'),

     url(r'^(?P<issue_id>\d+)/$', 'viewIssue', name="IssueTracker-view"),
     url(r'^(?P<issue_id>\d+)/modIssue/', 'modIssue', 
         name='IssueTracker-modIssue'),

     url(r'^history/(?P<item_id>\d+)/$', 'history', name="IssueTracker-history"),
     url(r'^history/(?P<item_id>\d+)/(?P<page>\d+)/$', 'history', 
         name="IssueTracker-history-page"),
)

urlpatterns += patterns("IssueTracker.views.reports",
     url(r'^report/all/$', 'allUnresolved', name='viewAll'),
     url(r'^report/all/(?P<page>\d+)/$', 'allUnresolved', name='viewAll'),

     url(r'^report/group/(?P<group_by>\w+)/$', 'groupedList', name='groupView'),
     url(r'^report/group/(?P<group_by>\w+)/(?P<page>\d+)/$', 'groupedList', 
         name='groupView'),
)


urlpatterns += patterns('IssueTracker.views.search',
     url(r'^search/$', 'search', name="issueSearch"),
     # (r'^search/detailed/$', 'advSearch'),
)

urlpatterns += patterns('IssueTracker.views.ajax',
    (r'^checkuser/(?P<name>\w+)/$', 'userCheck'),

    (r'^search/field/(?P<field_name>\w+)/$', 'getSearchField'),

    (r'^groups/$', 'getGroups'),
    (r'^items/$', 'getItems'),
    (r'^invSpec/create/$', 'invSpecCreate'),
)
