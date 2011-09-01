import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils
import Tracker.models as t_models
import Viewer.models as v_models
import LabtrackerCore.utils as utils

from Viewer.forms import TimeForm, FileTimeForm
from Viewer.utils import getStats, cacheStats

from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
import time
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

try:
    set
except NameError:
    from sets import Set as set
from decimal import *

# User must have same permissions to add statistics in order to download them. (At this time, only staff)
@permission_required('Viewer.add_labstats', login_url='/login/')
def allStatsFile(request):
    """
    Get a file of lab statistics within time frame.
    Default is current week.
    """
    begin = None
    end = None
    form = FileTimeForm()
    data = None
    response = None
    message = None

    if request.GET.has_key('time_start') and request.GET.has_key('time_end'):
        form = FileTimeForm(request.GET)
        if form.is_valid():
            end = request.GET['time_end']
            end_date, end_time = end.split()
            begin = request.GET['time_start']
            begin_date, begin_time = begin.split()
     
           
            history = m_models.History.objects.values_list('user','login_time','session_time','machine').filter(login_time__gte=begin).exclude(login_time__gte=end)
            m_type = m_models.Type.objects.values_list('mt_id','name','platform').all()
            m_platform = m_models.Platform.objects.values_list('platform_id','name').all()
            m_machine = m_models.Item.objects.values_list('item_id','name','type','location').all()
            m_location = m_models.Location.objects.values_list('ml_id','name').all()
 
        if history == None:
            message =  "There is not data can be generated in this interval!"
        else:
            stats = []
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = "attachment; filename=LabStats_%s_to_%s.csv" % (begin_date, end_date)
            writer = csv.writer(response)

            for entry in m_location:
                machine_history = [ m for m in m_machine if m[3] == entry[0]]
                for each_m in machine_history:
                    type = [t for t in m_type if t[0] == each_m[2]][0]#return a tuple
                     
                    platform = [p[1] for p in m_platform if p[0] == type[2]][0]
                    location_history = [h for h in history if h[3]==each_m[0]]
                    for each in location_history:
                        stats.append([each[0],each_m[1],entry[1],each[1],each[2],type[1],platform])
            
            stats = sorted(stats, key= lambda s : s[3])
            for each in stats:
                writer.writerow([each[0],each[1],each[2],each[3],each[4],each[5],each[6]]) 
            return response
       
    


    args = {
        'form': form,
        'response':response,
        'message': message,
    }


    return render_to_response('LabStats/statsfile.html', args, context_instance=RequestContext(request))





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

    if not end:
       end = datetime.date.today()
       if not begin == end:
           begin = begin.date() 
    else:
       end = end.date()
       begin = begin.date()

    args = {
            'form': form,
            'location_stats': stats,
            'message': message,
            'begin': begin,
            'end':end,
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
