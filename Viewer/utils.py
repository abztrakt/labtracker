import Viewer.models as vm

from django.conf import settings as lset

import Machine.models as m_models

from django.db.models import Avg,Min, Max, Count, StdDev
try:
    set
except NameError:
    from sets import Set
from decimal import *

def makeFile(histories=None):
    """
    Generate the stats file from the given qDicts
    """
    stats = []
    for history in histories:
        data= {'user': history.user,
                'machine':  history.machine,
                'location': history.machine.location,
                'login_time': history.login_time,
                'session_time': history.session_time,
                'type': history.machine.type,
                'platform' : history.machine.type.platform}
        stats.append(data);
    return stats


def getStats(stats=None, machines=None, locations=None):
    """
    Generate general statistics from given qDicts
    """

    if not stats:
        stats = m_models.History.objects.filter(session_time__isnull=False)
    if not machines:
        machines = m_models.Item.objects.all()
    if not locations:
        locations = m_models.Location.objects.all()
 
    statistics = []
    login_count = 0


    #CHANGE
    #generate stats for all locations
    all_logins = 0
    all_machines = 0
    all_clients_count = 0
    all_data = stats.aggregate(min_time=Min('session_time'), max_time=Max('session_time'),avg_time=Avg('session_time'),total_time=Count('session_time'))

    # Generate stats for each location
    for location in locations:

        items = machines.filter(location=location)
        location_stats = stats.filter(machine__in=items, session_time__isnull=False)
        machines_in_location = items.count()
        
        if location_stats:

            # Login statistics
            login_count = login_count + location_stats.count()

            # Number of distinct clients
            clients_location = set()
            distinct_clients = [clients_location.add(stat.user) for stat in location_stats]

            # Seat time statistics
            data = location_stats.aggregate(min_time=Min('session_time'), max_time=Max('session_time'), avg_time=Avg('session_time'), total_time=Count('session_time'))

            logins_per_machine = 0
            distinct_per_machine = 0

            if machines_in_location != 0:
                distinct_per_machine = 1.0 * len(clients_location) / machines_in_location
                logins_per_machine = 1.0 * login_count / machines_in_location

            # Add to aggregation when we give sqlite3 std. dev. capabilities.
            data['stdev_time'] = 0
            if lset.DATABASE_ENGINE == 'mysql':
                stdev = location_stats.aggregate(stdev_time=StdDev('session_time'))
                data['stdev_time'] = "%.2f" % stdev['stdev_time']
            ###
            data['avg_time'] = "%.2f" % data['avg_time']
            data['location'] = location
            data['logins_per_machine'] = "%.2f" % logins_per_machine
            data['distinct_per_machine'] = "%.2f" % distinct_per_machine
            data['total_machines'] = machines_in_location
            data['total_logins'] = login_count
            data['distinct_logins'] = len(clients_location)
        
            statistics.append(data)

            #CHANGE get stats for all labs;
            #total_login
            all_machines = all_machines + machines_in_location
            all_logins = all_logins + login_count
            all_clients_count = all_clients_count + len(clients_location)
    all_logins_per_machine =1.0 *  all_logins / all_machines
    all_distinct_per_machine = 1.0 * all_clients_count / all_machines

    all_data['avg_time'] = "%.2f" % all_data['avg_time']
    all_data['location'] = "All labs"
    all_data['logins_per_machine'] = "%.2f" % all_logins_per_machine 
    all_data['distinct_per_machine'] = "%.2f" % all_distinct_per_machine
    all_data['total_machines'] = all_machines
    all_data['total_logins'] = all_logins
    all_data['distinct_logins'] = "%.2f" % all_distinct_per_machine
    all_data['stdev_time'] = 0
    if lset.DATABASE_ENGINE == 'mysql':
        stdev = stats.aggregate(stdev_time=StdDev('session_time'))
        all_data['stdev_time'] = "%.2f" % stdev['stdev_time']

    statistics.append(all_data)


    return statistics

def cacheStats(begin=None, end=None,labStats=True,tags=None, description=None):
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
    #change!! 
    #The call is from LabStats or StatsFile
    if labStats:
        if exists.count() > 0:
            return "This interval already exists!"
        if data:
            stats = getStats(data)
        else:
            return "There is no data to save in this interval!"

        return "Your entry has been successfully saved."
    else:
        if not data:
            return "There is no file can be generated in this interval!"

def getViewType(name):
    namespace = name.split('.')[-1]
    return vm.ViewType.objects.get(name=namespace)
