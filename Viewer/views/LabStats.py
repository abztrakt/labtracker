import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils
import Tracker.models as t_models
import Viewer.models as v_models
import LabtrackerCore.utils as utils

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

        args = utils.generatePageList(request, entries, 1)
        args['tags'] = v_models.Tags.objects.all()
        
        entry_duplicates = {}
        args['objects'] = list(args['objects'])

        for entry in args['objects']:
            time = entry.time_start.__str__()
            if time in entry_duplicates:
                entry_duplicates[time] = entry_duplicates[time] + 1
            else:
                entry_duplicates[time] = 1

        for entry in args['objects']:
            time = entry.time_start.__str__()
            if entry_duplicates[time] > 1:
                entry_duplicates[time] = entry_duplicates[time] - 1
                args['objects'].remove(entry)

        return render_to_response('LabStats/cache_list.html', args, context_instance=RequestContext(request))
    
    else:
        entry = v_models.StatsCache.objects.filter(time_start=begin, time_end=end)
        for data in entry:
            data.logins_per_machine = "%.2f" % (float(data.total_logins) / data.total_items)
            data.distinct_per_machine = "%.2f" % (float(data.total_distinct) / data.total_items)

        args = {
                'title': begin + " to " + end,
                'entry': entry
            }

        return render_to_response('LabStats/cache_page.html', args, context_instance=RequestContext(request))
