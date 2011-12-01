from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Avg, Min, Max, Count
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

        #Calculate stats for each area. 
        locations = Location.objects.all().order_by('name')
        stats = []
        overall = {    
                'Location': 'OVERALL',
                'Status': '',
                'Total': 0,
                'inUse': 0,
                'Broken': 0,
                'Usable': 0,
                'Unusable': 0,
                'MagicNum': 0,
                'Threshold': 'N/A',
                'ThresholdComps': 0,
                'ThresholdMessage': '',
                'LabLoad' : 0.0,
                'PerUsable': 0.0,
                'PercBroken': 0.0,
                'PercUnusable': 0.0
            }
        for location in locations:
            #Grab only machines in the location.
            machines = Item.objects.filter(location=location).exclude(retired=True)    
            if machines:
                #We have machines in the location, calculate data and place defaults into a dictionary. Separate out calculated data and static data. Add/remove stats for any future dashboard calcs.
                data = {    
                    'Location': location,
                    'Status': 'ok',
                    'Total': machines.count(),
                    'inUse': 0,
                    'Broken': 0,
                    'Usable': 0,
                    'Unusable': 0,
                    'MagicNum': 0,
                    'Threshold': location.usable_threshold,
                    'ThresholdComps': 0,
                    'ThresholdMessage': '',
                    'LabLoad' : 0.0,
                    'PerUsable': 0.0,
                    'PercBroken': 0.0,
                    'PercUnusable': 0.0,
                    'warning_threshold':0.0,
                    'red': 255,
                    'green': 0
                }

                overall['Total'] += data['Total']

                # Loop trough the machines and tally up their statuses.
                for machine in machines:
                    if not machine.retired:
                        statuses = machine.status.values_list()
                        unresolved = machine.unresolved_issues()

                        #Calculate statuses
                        for status in statuses:
                            if status[0] == 1:
                                #Machine is INUSE, add to the inuse value.
                                data['inUse'] += 1
                                overall['inUse'] += 1
                        
                        #Check to see if machine is BROKEN (has issues), if so, add to the broken value
                        if unresolved.count() != 0:
                            data['Broken'] += 1
                            overall['Broken'] += 1
                        
                        #Check if machine is USABLE, or not.
                        if machine.unusable:
                            data['Unusable'] += 1
                            overall['Unusable'] += 1
                        else:
                            data['Usable'] += 1
                            overall['Usable'] += 1

                #Calculate percentages after the tallying.
                if data['Usable'] != 0:
                    data['LabLoad'] = round((100.0 * data['inUse']/data['Usable']), 2)
                data['PercUsable'] = round((100.0 * data['Usable']/data['Total']), 2)
                data['PercBroken'] = round((100.0 * data['Broken']/data['Total']), 2)
                data['PercUnusable'] = round((100.0 * data['Unusable']/data['Total']), 2)

                #Calculate the "magic number" for the location, and the number of comps needed to be in threshold.
                data['ThresholdComps'] = int(round((data['Threshold']/ 100.0) * data['Total'], 0))
                overall['ThresholdComps'] += data['ThresholdComps']
                data['MagicNum'] = int(data['Usable'] - data['ThresholdComps'])
                data['warning_threshold']=round((100.0-data['Threshold'])/2, 2)
                puot= round(data['PercUsable']-data['Threshold'], 2)
                if data['MagicNum'] < 0:
                    #We are under threshold, leave a fix message
                    data['ThresholdMessage'] = 'Fix %i' % (data['MagicNum']*-1)
                    data['MagicNum'] *= -1
                elif data['MagicNum'] == 0:
                    #We are AT threshold
                    data['ThresholdMessage'] = 'At threshold'
                else:
                    #We are above the threshold
                    data['ThresholdMessage'] = '+%i above threshold' % (data['MagicNum'])
                if (data['PercUsable']> data['Threshold']):
                    if (data['warning_threshold'] > puot):
                        data['green']=int(255*round(puot/(data['warning_threshold']), 2))
                    elif (data['warning_threshold'] <=  puot):
                        data['red']=int(255.0 -255*round((puot-data['warning_threshold'])/(100-data['Threshold']-data['warning_threshold']), 2))
                        data['green']=255 
                #Keep track of css colors for each location threshold. (i.e. ok = above or at threshold in one aera, etc...)
                if data['PercUsable'] <= data['Threshold']:
                    #We are BELOW threshold, color this red
                    data['Status'] = 'problem'
                    overall['MagicNum'] += data['MagicNum']
                
                #Finally, append all data to the stats
                stats.append(data)

        #After calculating numerical stats, tally up an OVERALL stat and add to the stats.
        # Calculate percentages. In the case that some of the division is by 0, ignore it and leave at the default.
        try:
            try:
                overall['LabLoad'] = round(100.0 * overall['inUse'] / overall['Usable'], 2)
            except:
                overall['LabLoad'] = 0.0
            overall['PercUsable'] = round(100.0 * overall['Usable'] / overall['Total'], 2)
            overall['PercBroken'] = round(100.0 * overall['Broken'] / overall['Total'], 2)
            overall['PercUnusable'] = round( 100.0 * overall['Unusable'] / overall['Total'], 2)
        except:
            overall['PercUsable'] = 0.0 
            overall['PercBroken'] = 0.0
            overall['PercUnusable'] = 0.0
        if overall['MagicNum'] > 0:
            overall['ThresholdMessage'] = 'Fix %i' % (overall['MagicNum'])
        else:
            overall['ThresholdMessage'] = 'At or above threshold'
        stats.append(overall)

        #Login 
        prev_logins = None
        if request.user.is_staff:
            userhash = md5(request.user.username)
            try:
                user = LabUser.objects.get(pk=userhash.hexdigest())
                prev_logins = History.objects.filter(user=user).order_by('-login_time')[:10]
            except Exception, e:
                pass

        return render_to_response('dashboard.html', {'problems': assigned, 'prev_logins': prev_logins,'recent_issues': recent_issues,'stats': stats},
                context_instance=RequestContext(request))
    
    else:
        return redirect('/login/')
