import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils
import Tracker.models as t_models

from Tracker.utils import getStats

from django.shortcuts import render_to_response
from django.template import RequestContext
from sets import Set
import datetime
import time

def allStats(request):
    """
    Get a summary of lab statistics within time frame.
    Default is current week.
    """
    today = datetime.date.today().weekday()
    begin = datetime.date.today()
    timestamp = time.mktime(begin.timetuple())
    if today != 6: # Today is not Sunday, otherwise display today's stats
        timestamp = timestamp - (1 + today) * 24 * 60 * 60
        begin = datetime.datetime.fromtimestamp(timestamp)

    stats = t_models.Statistics.objects.filter(login_time__gte=begin)

    args = {
            'location_stats': getStats(stats)
        }
    
    return render_to_response('labstats.html', args, context_instance=RequestContext(request));
