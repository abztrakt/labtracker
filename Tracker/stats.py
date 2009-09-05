import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils
import Tracker.models as t_models

from Tracker.forms import TimeForm
from Tracker.utils import getStats

from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
import time

def allStats(request):
    """
    Get a summary of lab statistics within time frame.
    Default is current week.
    """
    stats = t_models.Statistics.objects.all()
    data = request.REQUEST.copy()
    begin = None
    end = None
    form = TimeForm()

    # Find a way to cache statistics using the same form submission
    if request.method == 'POST':
        form = TimeForm(request.POST)
        if form.is_valid():
            end = form.cleaned_data['time_end']
            begin = form.cleaned_data['time_start']
            """
            if form contains process_cache;
                use begin and end dates to pass into cache function
                display a confirmation message if successful
            """

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

    args = {
            'form': form,
            'location_stats': getStats(stats)
        }

    if not stats:
        args['location_stats'] = None

    return render_to_response('labstats.html', args, context_instance=RequestContext(request));
