import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils
import Tracker.models as t_models
import Viewer.models as v_models
import LabtrackerCore.utils as utils

from Viewer.forms import TimeForm, FileTimeForm
from Viewer.utils import getStats, cacheStats,makeFile

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

    GET_begin_date = request.GET.get('time_start_0','') 
    GET_begin_time = request.GET.get('time_start_1','')
    GET_begin = GET_begin_date + ' ' + GET_begin_time

    GET_end_date = request.GET.get('time_end_0','')
    GET_end_time = request.GET.get('time_end_1','')
    GET_end = GET_end_date + ' ' + GET_end_time

    if not GET_begin == ' ' and not GET_end == ' ':
        form = FileTimeForm(request.GET)
        if form.is_valid():
            end = form.cleaned_data['time_end']
            begin = form.cleaned_data['time_start'];
     
            
            data = m_models.History.objects.select_related().filter(login_time__gte=begin).exclude(login_time__gte=end)
            
        if data == None:
            message =  "There is not data can be generated in this interval!"
        else:
            stats = []
            for history in data:
                data= {'user': history.user,
                        'machine':  history.machine,
                        'location': history.machine.location,
                        'login_time': history.login_time,
                        'session_time': history.session_time,
                        'type': history.machine.type,
                        'platform' : history.machine.type.platform}
                stats.append(data)
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=LabStat'+GET_begin_date + '__'+GET_end_date+' .csv'
            writer = csv.writer(response)
            
            for entry in stats :
                writer.writerow(entry[user],entry[machine],entry[location],entry[login_time],entry[session_time],entry[type],entry[platform])
                
                
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
