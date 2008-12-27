# Django settings for labtracker project.

DEBUG = True 
TEMPLATE_DEBUG = DEBUG
USE_I18N = False

APP_DIR = "/var/www/django_apps/labtracker"

ADMINS = (
        ('Jane Doe', 'jd@u.washington.edu'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'                # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'labtracker'             # Or path to database file if using sqlite3.
DATABASE_USER = 'labtracker'             # Not used with sqlite3.
DATABASE_PASSWORD = 'SECURITYPLUSPLUS'   # Not used with sqlite3.
DATABASE_HOST = 'localhost'              # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '3306'                   # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

SITE_ADDR = "http://example.com"
SECURE_ADDR = "https://example.com"

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/static/' % APP_DIR

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '%s/static/' % SITE_ADDR

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '%s/media_admin/' % SITE_ADDR

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'burnjv1*nnb+#55vh%40ggvgm31@!y#njt3)#2n+(b%z1d-zz&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    #"django.core.context_processors.i18n",
    "django.core.context_processors.media"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'labtracker.auth.ActiveDirectoryBackend',
    'django.contrib.auth.backends.ModelBackend'
)

ROOT_URLCONF = 'labtracker.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/templates' % APP_DIR,
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
    'django.contrib.admin',
    'labtracker.LabtrackerCore',
    'labtracker.Machine',
    'labtracker.IssueTracker',
    'labtracker.Viewer',
    'labtracker.Tracker',
)

LOGIN_URL="/issue/login/"
LOGIN_REDIRECT_URL="/"

EMAIL_HOST="localhost"
EMAIL_PORT=25
DEFAULT_FROM_EMAIL="labtracker@localhost"
EMAIL_TEST_RECIPIENT="test@localhost"

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
