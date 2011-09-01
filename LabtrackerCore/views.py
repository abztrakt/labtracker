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
            all_locations[location.name] = {'Total': 0, 'inUse':0, 'Broken':0,'Usable':0,'Unusable':0}

        all_locations['OVERALL'] = {'Total': 0, 'inUse':0, 'Broken':0,'Usable':0,'Unusable':0}

        # Loop through the machines and tally up their statuses. 
        for machine in all_machines:
            location = machine.location.name
            statues = machine.status.values_list()
            usable = False 
            for status in statues:
                if status[0] == 3:
                    #Machine is USABLE, add to usable value.
                    usable = True
                if status[0] == 2:
                    #Machine is BROKEN, add to the broken value.
                    all_locations[location]['Broken'] += 1
                    all_locations['OVERALL']['Broken'] += 1
                if status[0] == 1:
                    #Machine is INUSE, add to the inuse value.
                    all_locations[location]['inUse'] += 1
                    all_locations['OVERALL']['inUse'] += 1

            all_locations[location]['Total'] += 1
            all_locations['OVERALL']['Total'] += 1

            if usable:
                all_locations[location]['Usable'] += 1
                all_locations['OVERALL']['Usable'] += 1
            else:
                all_locations[location]['Unusable'] += 1
                all_locations['OVERALL']['Unusable'] += 1

        # Calculate the percentages at each location (including OVERALL) and then drop any that have a 0 Total
        empty_locations = []
        for location in all_locations:
            try:
                all_locations[location]['LabLoad'] = "%.0f" % (100.0 * (all_locations[location]['inUse'])/all_locations[location]['Usable'])
                all_locations[location]['PercUsable'] = "%.0f" % (100.0 * (all_locations[location]['Usable'])/all_locations[location]['Total'])
                all_locations[location]['PercBroken'] = "%.0f" % (100.0 * (all_locations[location]['Broken'])/all_locations[location]['Total'])
                all_locations[location]['PercUnusable'] = "%.0f" % (100.0 * (all_locations[location]['Unusable'])/all_locations[location]['Total'])

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

        overall = all_locations.pop('OVERALL')

        return render_to_response('dashboard.html', {'problems': assigned, 'prev_logins': prev_logins,'recent_issues': recent_issues,'all_locations': all_locations, 'overall': overall,},
                context_instance=RequestContext(request))
    
    else:
        return redirect('/login/')
