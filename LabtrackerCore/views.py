from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

@login_required
def userPrefs(request):
    """
    User preference pane, may be renamed later
    """
    return render_to_response('user_prefs.html', {}, 
            context_instance=RequestContext(request))
