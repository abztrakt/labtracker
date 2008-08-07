from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required

from IssueTracker.models import Issue
from LabtrackerCore.models import Item as Core 
from Machine.models import Item as Machine

@permission_required('IssueTracker.can_view', login_url="/login/")
def history(request, machine_name):
    """
    Grab all the tickets for this particular machine and display
    """
    core = get_object_or_404(Core, name=machine_name) 
    issues = Issue.objects.filter(item=core).order_by('-post_time')
    machine = Machine.objects.get(core=core) 

    return render_to_response('IssueTracker/history.html', 
                {'machine': machine, 'issues': issues}, 
                    context_instance=RequestContext(request))
