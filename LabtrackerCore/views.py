from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from LabtrackerCore.forms import EmailForm

from IssueTracker.models import Issue

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


@login_required
def dashboard(request):
    """
    Displays the (arguably) most useful data on the first page.
    May be customizable in the future.
    """

    # User's assigned issues
    assigned = Issue.objects.all().filter(assignee=request.user.id).order_by('-post_time')[:5]

    #TODO Add general usage statistics here

    
    return render_to_response('dashboard.html', {'problems': assigned},
            context_instance=RequestContext(request))

