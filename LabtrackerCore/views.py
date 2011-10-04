from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

from LabtrackerCore.forms import EmailForm

from LabtrackerCore.models import LabUser
from IssueTracker.models import Issue
from Machine.models import History, Item, Location
from hashlib import md5

@login_required
def userPrefs(request):
    """
    User preference pane, may be renamed later
    """
    args = { "messages": [] }

    if request.method == "POST":
        data = request.POST.copy()

        args['emailForm'] = EmailForm(data, instance=request.user)

        if args['emailForm'].is_valid():
            args['emailForm'].save()
            args['messages'].append("Email succesfully saved")

    else:
        args['emailForm'] = EmailForm(instance=request.user)


    return render_to_response('user_prefs.html', args, 
            context_instance=RequestContext(request))


def dashboard(request):
    """
    Displays the (arguably) most useful data on the first page.
    May be customizable in the future.
    """

    if request.user.is_authenticated():
        # User's assigned issues
        assigned = Issue.objects.filter(assignee=request.user.id).order_by('-post_time')[:5]
        # The 5 most recently created issues.
        recent_issues = Issue.objects.all().order_by('-post_time')[:5]
        # All machines in the system.
        all_machines = Item.objects.all()

        # Initiate a list of all locations and their stats.
        all_locations = {}
        for location in Location.objects.all():
            all_locations[location.name] = {'Total': 0, 'inUse':0, 'Broken':0,'Usable':0,'Unusable':0, 'MagicNum':0}

        all_locations['OVERALL'] = {'Total': 0, 'inUse':0, 'Broken':0,'Usable':0,'Unusable':0, 'MagicNum':0}

        # Loop through the machines and tally up their statuses. 
        for machine in all_machines:
            if not machine.retired:
                location = machine.location.name
                statues = machine.status.values_list()
                unresolved = machine.unresolved_issues()
                unusable = machine.unusable
                for status in statues:
                    if status[0] == 1:
                        #Machine is INUSE, add to the inuse value.
                        all_locations[location]['inUse'] += 1
                        all_locations['OVERALL']['inUse'] += 1

                #Machine is BROKEN, add to the broken value.
                if unresolved.count() != 0:
                    all_locations[location]['Broken'] += 1
                    all_locations['OVERALL']['Broken'] += 1

                all_locations[location]['Total'] += 1
                all_locations['OVERALL']['Total'] += 1

                #Machine is USABLE, add to usable value.
                if not unusable:
                    all_locations[location]['Usable'] += 1
                    all_locations['OVERALL']['Usable'] += 1
                #Machine is UNUSABLE, add to unusable value.
                else:
                    all_locations[location]['Unusable'] += 1
                    all_locations['OVERALL']['Unusable'] += 1

        # Calculate the percentages at each location (including OVERALL) and then drop any that have a 0 Total
        empty_locations = []
        for location in all_locations:
            try: 
                all_locations[location]['LabLoad'] = float("%.02f" % (100.0 * (all_locations[location]['inUse'])/all_locations[location]['Usable']))
            except ZeroDivisionError:
                all_locations[location]['LabLoad'] = 0.0
            
            try:
                all_locations[location]['PercUsable'] = float("%.02f" % (100.0 * (all_locations[location]['Usable'])/all_locations[location]['Total']))
                all_locations[location]['PercBroken'] = float("%.02f" % (100.0 * (all_locations[location]['Broken'])/all_locations[location]['Total']))
                all_locations[location]['PercUnusable'] = float("%.02f" % (100.0 * (all_locations[location]['Unusable'])/all_locations[location]['Total']))
                
                #Keeps track of the " magic number" (number of machines needed to be fixed/broken in order to go below/above threshold).
                if location != 'OVERALL':
                    tempUsable = all_locations[location]['PercUsable']
                    if all_locations[location]['PercUsable'] >= Location.objects.get(name=location).usable_threshold:
                        while (tempUsable >= Location.objects.get(name=location).usable_threshold):
                            all_locations[location]['MagicNum'] += 1
                            tempUsable = float("%.02f" % (100.0 * ((all_locations[location]['Usable'])-(all_locations[location]['MagicNum']))/all_locations[location]['Total']))
                    else:
                        while (tempUsable < Location.objects.get(name=location).usable_threshold):
                            all_locations['OVERALL']['MagicNum'] += 1
                            all_locations[location]['MagicNum'] += 1
                            tempUsable = float("%.02f" % (100.0 * ((all_locations[location]['Usable'])+(all_locations[location]['MagicNum']))/all_locations[location]['Total']))

                #Keep track of css colors for each location threshold. (i.e. green = 95% in one area, etc..)
                try:
                    if all_locations[location]['PercUsable'] >= Location.objects.get(name=location).usable_threshold:
                        all_locations[location]['ok'] = True
                    else:
                        all_locations[location]['ok'] = False
                except Location.DoesNotExist:
                    pass

            except ZeroDivisionError:
                empty_locations.append(location)
        
        for location in empty_locations:
            del all_locations[location]
        
        prev_logins = None
        if request.user.is_staff:
            userhash = md5(request.user.username)
            try:
                user = LabUser.objects.get(pk=userhash.hexdigest())
                prev_logins = History.objects.filter(user=user).order_by('-login_time')[:10]
            except Exception, e:
                pass
        
        # Removes the row of overall stats from the saved locations and saves it
        overall = all_locations.pop('OVERALL')

        # Forms a list of the location dictionaries.
        all_locations_sorted = []
        for location in all_locations:
            all_locations[location]['Location'] = location.encode('utf-8')
            all_locations_sorted.append(all_locations[location])

        return render_to_response('dashboard.html', {'problems': assigned, 'prev_logins': prev_logins,'recent_issues': recent_issues,'all_locations': all_locations_sorted, 'overall': overall,},
                context_instance=RequestContext(request))
    
    else:
        return redirect('/login/')
