from django.conf.urls.defaults import *

import IssueTracker.signals

urlpatterns = patterns('',
    url(r'^$', 'LabtrackerCore.views.userPrefs', name='userPrefs'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^pwchange/$', 'password_change', 
        {'template_name': 'pwchange.html'}, name="pwchange"),
    (r'^pwchange/done/$', 'password_change_done', {'template_name': 'pwchange_done.html'}),
)
