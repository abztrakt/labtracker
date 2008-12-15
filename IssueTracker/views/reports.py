from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response

import IssueTracker.utils as utils
import IssueTracker.models as im

@permission_required('IssueTracker.can_view', login_url="/login/")
def allUnresolved(request, page=1):
    """
    Lists all the Issues 
    """
    args = utils.generatePageList(request, 
            im.Issue.objects.filter(resolved_state__isnull=True), page)

    args['object_list'] = args['page'].object_list

    return render_to_response("issue_list.html", args,
            context_instance=RequestContext(request))

@permission_required('IssueTracker.can_view', login_url="/login/")
def groupedList(request, group_by=None, page=1):
    """
    Lists issues, group_by
    """

    if group_by not in ('problem_type','reporter', 'item'):
        return Http404()

    objects = im.Issue.objects.filter(resolved_state__isnull=True)\
            .order_by(group_by)

    args = utils.generateIssueArgs(request, objects)

    # do the group by
    issue_list = {}
    for issue in args['issues']:
        field = getattr(issue, group_by)

        if type(field).__name__ == "ManyRelatedManager":
            qs = field.get_query_set()
            group_names = [item.name for item in qs]
        else:
            group_names = [field]

        for group_name in group_names:
            if issue_list.has_key(group_name):
                issue_list[group_name].add(issue)
            else:
                issue_list[group_name] = set([issue,])

    args['object_list'] = issue_list

    return render_to_response("grouped_issue_list.html", args,
            context_instance=RequestContext(request))
