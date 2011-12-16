# Local settings for labtracker project.
# Copy this file to 'local_settings.py' and customize for your instance.
# If you wish to override anything else that is in the settings.py, just add it here!

DEBUG = True

APP_DIR = "/path/to/your/django/sites/labtracker"
SITE_ADDR = "http://localhost:8000"
SECURE_ADDR = "http://localhost:8000"

ADMINS = (
    # ('YOUR NAME', 'YOUR EMAIL'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'labtracker.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e)_-c_)2kts$t2b5gvc7l55&b7ltf0l5e)pkzet%oabi-_k6y6'

### Things below this line need to be in the local_settings, but you shouldn't have to change them.

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '%s/static/' % APP_DIR

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '%s/static/' % SITE_ADDR

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/static/" % APP_DIR,
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/templates" % APP_DIR,
)

FIXTURE_DIRS = (
    '%s/tests/fixtures/'  % APP_DIR,
)
