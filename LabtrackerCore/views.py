from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

from LabtrackerCore.forms import EmailForm

from LabtrackerCore.models import LabUser
from IssueTracker.models import Issue
from Machine.models import History
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
        prev_logins = None
        #TODO Add general usage statistics here
        if request.user.is_staff:
            userhash = md5(request.user.username)
            try:
                user = LabUser.objects.get(pk=userhash.hexdigest())
                prev_logins = History.objects.filter(user=user).order_by('-login_time')[:10]
            except Exception, e:
                pass

        return render_to_response('dashboard.html', {'problems': assigned, 'prev_logins': prev_logins},
                context_instance=RequestContext(request))
    
    else:
        return redirect('/login/')
