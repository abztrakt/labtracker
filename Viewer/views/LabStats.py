import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils
import Tracker.models as t_models
import Viewer.models as v_models

from Viewer.forms import TimeForm
from Viewer.utils import getStats, cacheStats

from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
import time

from sets import Set
from decimal import *

def allStats(request):
    """
    Get a summary of lab statistics within time frame.
    Default is current week.
    """
    stats = m_models.History.objects.all()
    data = request.REQUEST.copy()
    begin = None
    end = None
    form = TimeForm()
    message = None

    # Find a way to cache statistics using the same form submission
    if request.method == 'POST':
        form = TimeForm(request.POST)
        if form.is_valid():
            end = form.cleaned_data['time_end']
            begin = form.cleaned_data['time_start']
            cache = form.cleaned_data['cache_interval']

            if cache:
                message = cacheStats(begin, end)

    if not begin:
        today = datetime.date.today().weekday()
        begin = datetime.date.today()
        timestamp = time.mktime(begin.timetuple())
        if today != 6: # Today is not Sunday, otherwise display today's stats
            timestamp = timestamp - (1 + today) * 24 * 60 * 60
            begin = datetime.datetime.fromtimestamp(timestamp)
        
    elif end:
        stats = stats.exclude(login_time__gte=end)

    stats = stats.filter(login_time__gte=begin)

    if stats:
        stats = getStats(stats)
    else:
        stats = []

    args = {
            'form': form,
            'location_stats': stats,
            'message': message
        }

    if not stats:
        args['location_stats'] = None

    return render_to_response('LabStats/labstats.html', args, context_instance=RequestContext(request))

def showCache(request, begin=None, end=None):
    """
    Displays all previously cached results
    """
    if not begin and not end:
        entries = v_models.StatsCache.objects.all().order_by('-time_start')

        time = {}
        for entry in entries:
            entry.time_start = str(entry.time_start)
            entry.time_end = str(entry.time_end)
            if not entry.time_start in time or not (entry.time_end == time[entry.time_start]):
                time[entry.time_start] = entry.time_end

        entries = []
        for key, value in time.iteritems():
            entry = {
                    'time_start': key,
                    'time_end': value
                }
            entries.append(entry)

        args = {
                'time': entries
            }

        return render_to_response('LabStats/cache_list.html', args, context_instance=RequestContext(request))
    
    else:
        entry = v_models.StatsCache.objects.filter(time_start=begin, time_end=end)
        for data in entry:
            data.logins_per_machine = Decimal(data.total_logins) / Decimal(data.total_items)
            data.distinct_per_machine = Decimal(data.total_distinct) / Decimal(data.total_items)

        args = {
                'title': begin + " to " + end,
                'entry': entry
            }

        return render_to_response('LabStats/cache_page.html', args, context_instance=RequestContext(request))
