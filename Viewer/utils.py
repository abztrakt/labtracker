import Viewer.models as vm

from django.conf import settings as lset

import Machine.models as m_models

from django.db.models import Avg, Min, Max, Count, StdDev
from math import sqrt
from sets import Set
from decimal import *

def getStats(stats=None, machines=None, locations=None, threshold=None):
    """
    Generate general statistics from given qDicts
    """

    if not stats:
        stats = m_models.History.objects.filter(session_time__isnull=False)
    if not locations:
        locations = m_models.Location.objects.all()

    if not threshold:
        # TODO MOVE to settings.py. Currently hard coded. Threshold is in hours, convert to minutes
        threshold = 12.0 * 60 
    else:
        threshold *= 60

    statistics = []

    # Generate stats for each location
    for location in locations:
        login_count = 0

        #Determine if there is a certain group of machines to look for, or to look in all machines in the location
        if not machines:
            items = m_models.Item.objects.filter(location=location)
        else:
            items = machines.filter(location=location)

        machines_in_location = items.count()

        if machines_in_location:
            # We have machines in the location, calculate stats
            data = {}

            #Seperate out the login times and the session times (because a person can be logged in and not logged out during the time period)
            login_stats = stats.filter(machine__in=items)
            all_session_stats = stats.filter(machine__in=items, session_time__isnull=False)
            threshold_session_stats = all_session_stats.exclude(session_time__gt=str(threshold))

            if all_session_stats:
                # People have logged out of machines, calculate various session times
                total_data = all_session_stats.aggregate(min_time=Min('session_time'),all_max_time=Max('session_time'),all_avg_time=Avg('session_time'),all_total_time=Count('session_time'))
                threshold_data = threshold_session_stats.aggregate(max_time=Max('session_time'),avg_time=Avg('session_time'),total_time=Count('session_time'))

                # Combine data in threshold and all data (which includes large session times)
                data = dict(total_data.items() + threshold_data.items())
                data['avg_time'] = "%.2f" % data['avg_time']
                data['all_avg_time'] = "%.2f" % data['all_avg_time']

                if lset.DATABASE_ENGINE == 'mysql':
                    # Calculate standard deviation using django library (if applicable for the database)
                    stdev = threshold_session_stats.aggregate(stdev_time=StdDev('session_time'))
                    all_stdev = all_session_stats.aggregate(stdev_time=StdDev('session_time'))
                    data['stdev_time'] = "%.2f" % stdev['stdev_time']
                    data['all_stdev_time'] = "%.2f" % all_stdev['stdev_time']
                else:
                    # Database does not support standard deviation, calculate by hand
                    avg = data['avg_time']
                    all_avg = data['all_avg_time']
                    total = 0
                    all_total = 0
                    for session in all_session_stats:
                        n = pow((float(session.session_time) - float(avg)),2)

                        if session.session_time <= str(threshold):
                            total += n
                        all_total += n

                    stdev = sqrt(total / len(threshold_session_stats))
                    all_stdev = sqrt(all_total/ len(all_session_stats))
                    data['stdev_time'] = "%.2f" % stdev
                    data['all_stdev_time'] = "%.2f" % all_stdev
            else:
                data['min_time'] = "0"
                data['all_max_time'] = "0"
                data['all_avg_time'] = "0"
                data['all_total_time'] = "0"
                data['max_time'] = "0"
                data['total_time'] = "0"
                data['avg_time'] = "0"
                data['all_avg_time'] = "0"
                data['stdev_time'] = "0"
                data['all_stdev_time'] = "0"

            if login_stats:
                # People have logged into the machines
                login_count = login_stats.count()

                # Number of distinct clients
                clients_location = Set()
                distinct_clients = [clients_location.add(stat.user) for stat in login_stats]

                distinct_per_machine = 1.0 * len(clients_location) / machines_in_location
                logins_per_machine = 1.0 * login_count / machines_in_location

                # Store login calculations into dictionary
                data['logins_per_machine'] = "%.2f" % logins_per_machine
                data['distinct_per_machine'] = "%.2f" % distinct_per_machine
                data['total_logins'] = login_count
                data['distinct_logins'] = len(clients_location)

                # Append the last bits of information to the stats
                data['location'] = location
                data['total_machines'] = machines_in_location
                statistics.append(data)

    return statistics

def cacheStats(begin=None, end=None, tags=None, description=None,threshold=None):
    """
    Makes caches of statistics
    """
    # Default without parameters is the full previous week.
    if not begin and not end:
    # Define week begin and end
        today = datetime.date.today().weekday()
        begin = datetime.date.today()
        timestamp = time.mktime(begin.timetuple())
        if today != 6: # Today is not Sunday, otherwise display today's stats
            timestamp = timestamp - (1 + today) * 24 * 60 * 60
        
        end = datetime.datetime.fromtimestamp(timestamp)
        begin = datetime.datetime.fromtimestamp(timestamp - 7 * 24 * 60 * 60)

    data = m_models.History.objects.filter(login_time__gte=begin).exclude(login_time__gte=end)
    exists = vm.StatsCache.objects.filter(time_start=begin, time_end=end)

    if exists.count() > 0:
        return "This interval already exists!"
    if data:
        stats = getStats(data,threshold=threshold)
    else:
        return "There is no data to save in this interval!"
    # Make a row for each location, for each time interval
    for location in stats:
        interval = vm.StatsCache(location=location['location'], time_start=begin, time_end=end, mean_time=location['avg_time'], min_time=location['min_time'], max_time=location['max_time'], stdev_time=location['stdev_time'], total_time=location['total_time'], total_items=location['total_machines'], total_logins=location['total_logins'], total_distinct=location['distinct_logins'])
        interval.save()

    return "Your entry has been successfully saved."

def getViewType(name):
    namespace = name.split('.')[-1]
    return vm.ViewType.objects.get(name=namespace)
