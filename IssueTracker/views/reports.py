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

    return render_to_response("issue_list.html", args,
            context_instance=RequestContext(request))

@permission_required('IssueTracker.can_view', login_url="/login/")
def groupedList(request, group_by=None, page=1):
    """
    Lists issues, group_by
    """

    if group_by not in ('problem_type','reporter', 'item'):
        return Http404()

    objects = im.Issue.objects.filter(resolved_state__isnull=True)

    args = utils.generateIssueArgs(request, objects)

    # Sets do not preserve order, so we must use a list to store the items
    issue_list = {}
    issue_sets = {}     # need to use this to detect duplicates

    for issue in args['issues']:
        field = getattr(issue, group_by)

        if type(field).__name__ == "ManyRelatedManager":
            qs = field.get_query_set()
            group_names = [item.name for item in qs]
        else:
            group_names = [field]

        for group_name in group_names:
            if issue_list.has_key(group_name):
                # only add if it doesn't already exist in list
                if not issue_sets[group_name].issuperset([issue]):
                    issue_list[group_name].append(issue)
                    issue_sets[group_name].add(issue)
            else:
                issue_list[group_name] = [issue,]
                issue_sets[group_name] = set([issue,])

    items = issue_list.items()

    def tuple_sort(a, b):
        if a[0] == None:
            return -1
        elif b[0] == None:
            return 1

        return cmp(str(a[0]), str(b[0]))

    items.sort(tuple_sort)

    args['object_list'] = items

    return render_to_response("grouped_issue_list.html", args,
            context_instance=RequestContext(request))

