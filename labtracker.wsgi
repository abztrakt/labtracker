import os, sys


sys.path.append('/var/django_apps')
sys.path.append('/var/django_apps/labtracker')

os.environ['DJANGO_SETTINGS_MODULE'] = 'labtracker.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

