import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils
import Tracker.models as t_models

from django.shortcuts import render_to_response
from django.template import RequestContext
from sets import Set

def allStats(request):
    """
    Get a summary of all lab statistics
    """
    #TODO Define a display_by method and starting/ending times
    
    stats = t_models.Statistics.objects.all()
    machines = m_models.Item.objects.all()
    locations = m_models.Location.objects.all()
    
    # Total usage stats across all machines on campus
    total_uses = stats.filter(logout_time__isnull=False).count()
    total_machines = machines.count()
    
    # Stats for each location
    logins = []
    avgtime = []

    login_count = 0

    for location in locations:

        items = machines.filter(location=location)
        location_stats = stats.filter(item__in=items)
        machines_in_location = items.count()

        if machines_in_location != 0:
            lpm = location_stats.count() / machines_in_location
        else:
            lpm = 0
 
        # Number of distinct clients
        clients_location = Set()
        distinct_clients = [clients_location.add(stat.userid) for stat in location_stats]

        # Dictionary of logins per machine
        lpm = {
                'location': location,
                'logins': location_stats.count(), # login_time=True implied
                'machines': machines_in_location,
                'lpm': lpm,
                'clients': len(distinct_clients)
            }
        logins.append(lpm)
        
        # Seat time statistics
        min = 0
        max = 0
        mean = 0
        std = 0
        total = 0

        for value in location_stats:
            time = value.logout_time - value.login_time # Are these integers?
            # Calculate min
            if min > time:
                min = time
            # Calculate max
            if max < time:
                max = time
            # Calculate total
            total = total + time

        if machines_in_location != 0:
            mean = total / machines_in_location
        else:
            mean = 0
        
        data = {
                 'location': location,
                 'min': min,
                 'max': max,
                 'mean': mean,
                 'total': total
            }

        avgtime.append(data)

    args = {
            'logins': logins,
            'avgtime': avgtime,
            'total_uses': total_uses,
            'total_machines': total_machines
        }

    return render_to_response('labstats.html', args, context_instance=RequestContext(request));
