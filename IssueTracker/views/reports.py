from django.http import HttpResponseBadRequest
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage,InvalidPage

import Machine.models as mac
import IssueTracker.utils as utils
import IssueTracker.models as im

@permission_required('IssueTracker.can_view', login_url="/login/")
def allUnresolved(request, page=1):
    """
    Lists all the Issues, in-order by newest 
    """
    objects = im.Issue.objects.filter(resolved_state__isnull=True).reverse()
    
    
    args = utils.generatePageList(request, objects, page)
    args['issues'] = args['objects']
    
    args['no_results'] = args['page'].object_list.count() < 1

    return render_to_response("issue_list.html", args,
            context_instance=RequestContext(request))

@permission_required('IssueTracker.can_view', login_url="/login/")
def allBroken(request, page=1):
    """
    Lists all the Issues 
    """
    objects = im.Issue.objects.filter(resolved_state__isnull=True)
    args = utils.generatePageList(request, objects, page)
    args['issues'] = args['objects']
    issues_list = {'Issues on Unusable Machines':[]}
    for issue in args['issues']:
        iss_id = issue.item.item_id
        machine = mac.Item.objects.get(item_id=iss_id)

        if machine.unusable:
            issues_list['Issues on Unusable Machines'].append(issue)

    args['object_list'] = issues_list.items() 
    args['no_results'] = args['page'].object_list.count() < 1
    return render_to_response("grouped_issue_list.html", args,
            context_instance=RequestContext(request))


@permission_required('IssueTracker.can_view', login_url="/login/")
def groupedList(request, group_by=None, page=1):
    """
    Lists issues, group_by
    """

    if group_by not in ('problem_type','reporter', 'item', 'location', 'group', 'machine_type', 'platform'):
        return HttpResponseBadRequest()

    objects = im.Issue.objects.filter(resolved_state__isnull=True).reverse()

    args = utils.generateIssueArgs(request, objects)
    args['issues'] = args['objects']
    # Sets do not preserve order, so we must use a list to store the items
    issue_list = {}
    issue_sets = {}     # need to use this to detect duplicates
    for issue in args['issues']:
        group_names = []
        iss_id = issue.item.item_id
        machine = mac.Item.objects.get(item_id=iss_id)
        if group_by == 'location':
            location= str(machine.location) 
            group_names.append(location)
        elif group_by == 'group':
            group_names.append(str(issue.group))
        elif group_by == 'machine_type':
            group_names.append(str(machine.type))
        elif group_by == 'platform':
            group_names.append(str(machine.type.platform))
        else:
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
    
    args['no_results'] = len(items) < 1

    return render_to_response("grouped_issue_list.html", args,
            context_instance=RequestContext(request))

@permission_required('IssueTracker.can_view', login_url="/login/")
def filteredList(request, filter_by=None, filter_val=None, page=1):
    """
    Lists issues, filter
    """

    filter = {}

    if filter_by in ('assignee','reporter'):
        filter['assignee__username'] = filter_val
    else:
        return HttpResponseBadRequest()

    objects = im.Issue.objects.filter(resolved_state__isnull=True, **filter).reverse()

    args = utils.generatePageList(request, objects, page)
    args['issues'] = args['objects']

    args['no_results'] = args['page'].object_list.count() < 1

    return render_to_response("issue_list.html", args,
            context_instance=RequestContext(request))

@permission_required('IssueTracker.can_view', login_url="/login/")
def myissues(request, filter_by=None, filter_val=None, page=1):
    """
    Lists issues, filter
    """

    return filteredList(request, 'assignee', request.user.username)
