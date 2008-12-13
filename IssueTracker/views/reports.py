from django.http import HttpResponseRedirect, Http404, HttpResponse, \
        HttpResponseServerError
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404

import IssueTracker.utils as utils
import IssueTracker.models as im

@permission_required('IssueTracker.can_view', login_url="/login/")
def allUnresolved(request, page=1):
    """
    Lists all the Issues 
    """
    args = utils.generatePageList(request, 
            im.Issue.objects.filter(resolved_state__isnull=True), page)

    return render_to_response("issue_list.html", args,
            context_instance=RequestContext(request))

