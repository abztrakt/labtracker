from labtracker.LabtrackerCore import models as lm
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
     
) + patterns("IssueTracker.views.reports",
     url(r'^report/all/broken/$', 'allBroken', name='brokenView'),
     url(r'^report/all/$', 'allUnresolved', name='viewAll'),
     url(r'^report/all/(?P<page>\d+)/$', 'allUnresolved', name='viewAll'),

     url(r'^report/group/(?P<group_by>\w+)/$', 'groupedList', name='groupView'),
     url(r'^report/group/(?P<group_by>\w+)/(?P<page>\d+)/$', 'groupedList', 
         name='groupView'),

     url(r'^report/myissues/$', 'myissues', name='report-myissues'),
     url(r'^report/filter/(?P<filter_by>\w+)/(?P<filter_val>\w+)/$', 
        'filteredList', name='filteredView'), 
     
) + patterns('IssueTracker.views.search',
     url(r'^search/$', 'search', name="issueSearch"),
     # (r'^search/detailed/$', 'advSearch'), 

) + patterns('IssueTracker.views.ajax',
    (r'^checkuser/(?P<name>\w+)/$', 'userCheck'),

    (r'^search/field/(?P<field_name>\w+)/$', 'getSearchField'),

    (r'^groups/$', 'getGroups'),
    (r'^items/$', 'getItems'),
    (r'^invSpec/create/$', 'invSpecCreate'),

) + patterns('django.views.generic',
    (r'partial/(?P<object_id>\d+)/$', 'list_detail.object_detail', 
        { 'queryset': lm.Item.objects.all(), 
            "template_name": "partial/issue_list.html" }),
)

