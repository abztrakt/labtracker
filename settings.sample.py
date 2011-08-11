# Django settings for labtracker project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

APP_DIR = "/var/www/django_apps/labtracker"
SITE_ADDR = "http://example.com"
SECURE_ADDR = "https://example.com"

LOGIN_URL="/issue/login/"
LOGIN_REDIRECT_URL="/"

EMAIL_HOST="localhost"
EMAIL_PORT=25
DEFAULT_FROM_EMAIL="labtracker@localhost"
EMAIL_TEST_RECIPIENT="test@localhost"
#All E-mails sent will have the subject with this prefixed in brackets.
#E.G.: [LabTracker],[MyIssueTracker]
EMAIL_SUBJECT_PREFIX="LabTracker"

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'labtracker',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '%s/static/' % APP_DIR

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '%s/static/' % SITE_ADDR

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/static/" % APP_DIR,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e)_-c_)2kts$t2b^%vc7l35&b7l#z0l5e)pkznt%oabi-_k6y6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

"""
AUTHENTICATION_BACKENDS = (
    #'labtracker.auth.ActiveDirectoryBackend',
    #'labtracker.auth.UWRemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend'
    #'django.contrib.auth.backends.RemoteUserBackend',
)
"""

ROOT_URLCONF = 'labtracker.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/templates" % APP_DIR,
)

FIXTURE_DIRS = (
    '%s/tests/fixtures/'  % APP_DIR,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'labtracker.LabtrackerCore',
    'labtracker.Machine',
    'labtracker.IssueTracker',
    'labtracker.Viewer',
    'labtracker.Tracker',
    'south',
)

"""
### ACTIVE DIRECTORY SETTINGS

# AD_DNS_NAME should set to the AD DNS name of the domain (ie; example.com)  
# If you are not using the AD server as your DNS, it can also be set to 
# FQDN or IP of the AD server.
AD_DNS_NAME = "ldap.auth.server.net"
AD_LDAP_PORT = 389
AD_SEARCH_DN = 'searchdn'
AD_NT4_DOMAIN = 'something.wa.com'           # This is the NT4/Samba domain name
AD_SEARCH_FIELDS = ['sAMAccountName',]

AD_LDAP_URL = 'ldap://%s:%d' % (AD_DNS_NAME, AD_LDAP_PORT)
"""

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
