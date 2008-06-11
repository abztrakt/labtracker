from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^pwchange/$', 'django.contrib.auth.views.password_change', 
        {'template_name': 'pwchange.html'}, name="pwchange"),
    (r'^pwchange/done/$', 'django.views.generic.simple.redirect_to', {'url': '/pref/'}),
    url(r'^$', 'LabtrackerCore.views.userPrefs', name='userPrefs'),
)
