#!/usr/bin/python

from django.core.management import setup_environ
import settings

setup_environ(settings)

from labtracker.Viewer import utils
import time
import datetime


today = datetime.date.today().weekday()
begin = datetime.date.today()
timestamp = time.mktime(begin.timetuple())
if today != 6: # Today is not Sunday, otherwise display today's stats
    timestamp = timestamp - (1 + today) * 24 * 60 * 60
 
end = datetime.datetime.fromtimestamp(timestamp - 1) # Sat, 11:59:59 PM
begin = datetime.datetime.fromtimestamp(timestamp - 7 * 24 * 60 * 60) # Sun, 12:00:00 AM
message = utils.cacheStats(begin, end)
print "%s\nbegin: %s, end: %s" % (message, begin, end)
