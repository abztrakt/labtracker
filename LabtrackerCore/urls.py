from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^pwchange/$', 'django.contrib.auth.views.password_change', {'template_name': 'pwchange.html'}),
    (r'^pwchange/done/$', 'django.views.generic.simple.redirect_to', {'url': '/pref/'}),
    (r'^$', 'IssueTracker.views.user'),
)
