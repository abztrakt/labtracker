import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils
import Tracker.models as t_models

from sets import Set

def getStats(stats=None, machines=None, locations=None):
    """
    Generate general statistics from given qDicts
    """

    if not stats:
        stats = t_models.Statistics.objects.all()
    if not machines:
        machines = m_models.Item.objects.all()
    if not locations:
        locations = m_models.Location.objects.all()
 
    statistics = []
    login_count = 0

    # Generate stats for each location
    for location in locations:

        items = machines.filter(location=location)
        location_stats = stats.filter(item__in=items)
        machines_in_location = items.count()

        # Login statistics
        login_count = login_count + location_stats.count()

        # Number of distinct clients
        clients_location = Set()
        distinct_clients = [clients_location.add(stat.userid) for stat in location_stats]

        # Seat time statistics
        min = 0
        max = 0
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

        mean = 0
        logins_per_machine = 0
        distinct_per_machine = 0

        if location_stats:
            mean = total / len(location_stats)
        if machines_in_location != 0:
            distinct_per_machine = len(distinct_clients) / machines_in_location
            logins_per_machine = login_count / machines_in_location

        data = {
                'location': location,
                'min_minutes': min,
                'max_minutes': max,
                'mean_minutes': mean,
                'total_minutes': total,
                'logins_per_machine': logins_per_machine,
                'distinct_per_machine': distinct_per_machine,
                'total_machines': machines_in_location,
                'total_logins': login_count,
                'distinct_logins': len(distinct_clients)
        }
        statistics.append(data)

    return statistics

