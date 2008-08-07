from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from IssueTracker.models import Issue
from LabtrackerCore.models import Item as Machine



def history(request, machine_name):
    """
    Grab all the tickets for this particular machine and display
    """
    machine = get_object_or_404(Machine, name=machine_name) 
    issues = Issue.objects.filter(item=machine).order_by('-post_time')

    return render_to_response('IssueTracker/history.html', 
                {'machine': machine, 'issues': issues}, 
                    context_instance=RequestContext(request))
