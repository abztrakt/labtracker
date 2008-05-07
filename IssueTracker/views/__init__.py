from django import newforms as forms
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list
import django.db.models.loading as load

import simplejson

from IssueTracker.models import *
import LabtrackerCore.models as LabtrackerCore
from IssueTracker.forms import *
import IssueTracker.search as issueSearch
import IssueTracker.utils as utils

args = { 'loggedIn' : False, }

# XXX RequestContext processor?
def setDefaultArgs(request):
    """
    This is called by any view that needs to have default args set.
    """
    args['user'] = request.user

def index(request):
    """
    Used for log in as well
    """
    setDefaultArgs(request)

    return render_to_response('IssueTracker/index.html', args)

@permission_required('Issuetracker.add_issue', login_url="/login/")
def post(request, issue_id):
    """
    This is for posting comments, and modifying some things for issues after they are
    created.
    Requires a post request, otherwise nothing is done.
    """
    issue = get_object_or_404(Issue, pk=issue_id)


    #updateIssueForm = UpdateIssueForm(instance=issue)
    UpdateIssueForm = forms.form_for_instance(issue, fields=('problem_type',
        'assignee','cc','resolve_time', 'resolved_state', 'last_modified'))


    if request.method == 'POST':
        actionStr = []
        curAssignee = issue.assignee
        curState = issue.resolved_state
        data = request.POST.copy()

        #updateIssue = updateIssueForm(data)
        updateIssue = UpdateIssueForm(data)
        updateIssue = updateIssue.save(commit=False)


        if (data.has_key('cc')):
            # CC is special in that it only updates this area
            newUsers = User.objects.extra(where= [ 'id IN (%s)' % \
                    (", ".join(data.getlist('cc'))) ] ).order_by('id')
            curUsers = issue.cc.all().order_by('id')

            # find items that need to be removed
            # FIXME this is terrible inefficient, would be better if the newUsers list is shortened
            for curUser in curUsers:
                if curUser not in newUsers:
                    issue.cc.remove(curUser)

            # now curUsers only contains the users that need not be modified
            # add all newUsers not in curUser to cc list
            for newUser in newUsers:
                if newUser not in curUsers:
                    issue.cc.add(newUser)

        if data.has_key('assignee') and not (curAssignee == updateIssue.assignee):
            actionStr.append("Assigned to %s" % (updateIssue.assignee))
        if data.has_key('resolved_state') and not (curState == updateIssue.resolved_state):
            actionStr.append("Changed state to %s" % (updateIssue.resolved_state))

        if data.has_key('problem_type'):
            given_pt = {}

            # for each one that has been sent in args
            for g_pt in data.getlist('problem_type'):
                given_pt[int(g_pt)] = 1

            # Any problem type that is not given, will need to be marked for removal
            for pt in issue.problem_type.all():
                if not given_pt.has_key(pt.pk):
                    given_pt[pt.pk] = -1
                else:
                    # if it was given, and already exists, do nothing
                    given_pt[pt.pk] = 0

            drop_items = []
            add_items = []

            for pt in given_pt:
                item = ProblemType.objects.get(pk=pt)
                if given_pt[pt] == 1:
                    add_items.append(item.name)
                    issue.problem_type.add(item)
                elif given_pt[pt] == -1:
                    drop_items.append(item.name)
                    issue.problem_type.remove(item)

            hist_msg = ""
            if add_items:
                hist_msg += "<span class='label'>Added problems</span>: %s" % (", ".join(add_items))

                if drop_items:
                    hist_msg += "<br />"

            if drop_items:
                hist_msg += "<span class='label'>Removed problems</span>: %s" % (", ".join(drop_items))

            if hist_msg:
                utils.updateHistory(request.user, issue, hist_msg)
            


        if (actionStr):
            updateIssue.save()
            for action in actionStr:
                utils.updateHistory(request.user, issue, action)

        if data.has_key('comment') and (not (data['comment'] in ("", None))):
            data['user'] = str(request.user.id)
            data['issue'] = issue_id

            newComment = AddCommentForm(data)
            if newComment.is_valid():
                newComment = newComment.save()
            else:
                # Form not valid
                args['add_comment_form'] = newComment
    else:
        return Http404()

    return HttpResponseRedirect(reverse('view', args=[issue.issue_id]))

@permission_required('IssueTracker.add_issue', login_url="/login/")
def modIssue(request, issue_id):
    """
    Can be accessed through post or get, will redirect immediately afterwards
    """
    issue = get_object_or_404(Issue, pk=issue_id)
    postResp = {}

    if request.method == "POST":
        # POST means an ajax call and so will do a json response
        data = request.POST.copy()
    elif request.method == "GET":
        # direct call, will need to redirect
        data = request.GET.copy()

    if data['action'] == "dropcc":
        user = get_object_or_404(User, pk=int(data['user']))
        issue.cc.remove(user)
        utils.updateHistory(request.user, issue, "Removed %s from CC list" % (user))
        postResp['status'] = 1
    elif data['action'] == "addcc":
        user = get_object_or_404(User, username=data['user'])
        issue.cc.add(user)
        utils.updateHistory(request.user, issue, "Added %s to CC list" % (user))
        postResp['username'] = user.username
        postResp['userid'] = user.id
        postResp['status'] = 1

    # FIXME: Needs to deal with error handling here, what happens when user could not have
    # been removed?

    if data['js']:
        # means an ajax call and so will do a json response
        return HttpResponse(simplejson.dumps(postResp))
    else:
        # direct call, will need to redirect
        return HttpResponseRedirect(reverse('view', args=[issue.issue_id]))

@permission_required('IssueTracker.can_view', login_url="/login/")
def viewIssue(request, issue_id):
    """
    This is called when the issue requests a specific issue.
    Basically displays the requested issue and any related comments. Offers the
    user the ability to add comments to the issue.
    If a post is given, will also post a comment
    """
    setDefaultArgs(request)

    # get the issue
    issue = get_object_or_404(Issue, pk=issue_id)

    args['issue'] = issue
    args['history'] = IssueHistory.objects.filter(issue=issue).order_by('-time')
    args['comments'] = IssueComment.objects.filter(issue=issue).order_by('time')

    form = UpdateIssueForm(instance=issue)

    args['add_comment_form'] = AddCommentForm()
    args['update_issue_form'] = form
    args['problem_types'] = form.fields['problem_type'].queryset

    return render_to_response('IssueTracker/view.html', args)

@permission_required('IssueTracker.can_view', login_url="/login/")
def reportList(request):
    """
    Currently does nothing but will list out all the available queries to list available
    reports
    """
    setDefaultArgs(request)
    return render_to_response('IssueTracker/list.html', args)

@permission_required('IssueTracker.can_view', login_url="/login/")
def report(request, report_id):
    """
    View a specific report
    """
    setDefaultArgs(request)
    return render_to_response('IssueTracker/report.html', args)

@login_required
def user(request):
    """
    User preference pane, may be renamed later
    """
    setDefaultArgs(request)
    return render_to_response('IssueTracker/user.html', args)

@permission_required('IssueTracker.add_issue', login_url="/login/")
def createIssue(request):
    """
    This is the view called when the user is creating a new issue, not for 
    posting comments.
    Currently takes a request, and sets the reporter to whoever is logged in and
    then saves it.
    """
    # TODO improve the form validation here
    setDefaultArgs(request)

    if request.method == 'POST':
        data = request.POST.copy()          # need to do this to set some defaults
        data['reporter'] = str(request.user.id)

        form = CreateIssueForm(data)
        if form.is_valid():
            issue = form.save()
            return HttpResponseRedirect(reverse('view', args=[issue.issue_id]))
        else:
            # form was not valid, errors should be on form though, so nothing needs to be
            # done
            pass
    else:
        form = CreateIssueForm()

    args['form'] = form
    args['problem_types'] = form.fields['problem_type'].queryset
    return render_to_response('IssueTracker/create.html', args)

@permission_required('IssueTracker.can_view', login_url="/login/")
def search(request):
    """
    Takes a post, searches, and either redirects to a list of matching items (or no
    items), or the specific issue
    """
    setDefaultArgs(request)
    extra_context = {}

    if request.method == "POST":
        data = request.POST
    elif request.method == "GET":
        data = request.GET

    if data:
        # in this case, we get to process the stuff
        issue_id = data.get('search_term', False)

        if issue_id:
            try:
                issue_id = int(issue_id)

                issue = Issue.objects.get(pk=issue_id)
                return HttpResponseRedirect(reverse('view', args=[issue.issue_id]))
            except ValueError, e:
                # search_term was not an id, search by string
                issues = Issue.objects.filter(title__icontains=issue_id)

                return generateList(data, issues, 1)

            except ObjectDoesNotExist, e:
                # issue id was not an actual issue, use it as a search_term
                issues = Issue.objects.filter(title__contains=issue_id)

                # FIXME change so that it uses the generateList as well
                return generateList(data,
                        Issue.objects.all(), 1)

            except Exception, e:
                return HttpResponseServerError()

            #extra_context['error'] = 'Issue with id "%i" not found.' % issue_id
        else:
            return generateList(data, Issue.objects.all(), 1)


    else:
        return HttpResponseRedirect(reverse('index'))

@permission_required('IssueTracker.can_view', login_url="/login/")
def advSearch(request):
    """ advSearch

    Takes user to the advanced search form page
    """
    setDefaultArgs(request)

    """
    form = SearchForm()
    form.fields['resolved_state'].choices = [
            (state.pk, state.name) for state in ResolveState.objects.all()]
    form.fields['problem_type'].choices = [
            (type.pk, type.name) for type in ProblemType.objects.all()]
    form.fields['inventory_type'].choices = [
            (type.pk, type.name) for type in LabtrackerCore.InventoryType.objects.all()]

    args['form'] = form
    """
    if request.method == 'POST':
        data = request.POST.copy()
        if data['action'] == 'Search':
            # send the data to the search handler
            del(data['action'])
            del(data['fields'])
            searches = issueSearch.parseSearch(data)
            query = issueSearch.buildQuery(searches)

            extra_context = {}

            return HttpResponse(object_list(request, queryset=query, 
                extra_context = extra_context, allow_empty=True))


    args['add_query'] = AddSearchForm()

    return render_to_response('IssueTracker/adv_search.html', args)


@permission_required('IssueTracker.can_view', login_url="/login/")
def fetch(request, issue_id):
    """
    Fetch information for a given issue
    Needs request params:
        req     -- What data is being requested
        format  -- What format data should be returned in
    """
    issue = get_object_or_404(Issue, pk=issue_id)

    if request.method == "POST":
        data = request.POST.copy()
    elif request.method == "GET":
        data = request.GET.copy()

    if not data.has_key('req'):
        return Http404()

    req = data.get('req')
    format = data.get('format', 'xml')
    limit = data.get('limit', 0);

    if req == 'history':
        objs = IssueHistory.objects.filter(issue=issue).order_by('-time')

        if limit != 0:
            objs = objs[-limit:]

        req_data = utils.modelsToDicts(objs)
        pk = 'ih_id'

        if format == 'html':
            ii = 0
            for obj in objs:
                req_data[ii]['time'] = obj.time
                req_data[ii]['user'] = obj.user
                ii += 1

            template_args = { 'history': req_data }
               

    if format == 'json':
        # for security reasons, send hash not list
        f_data = {}
        for piece in req_data:
            f_data[piece[pk]] = piece
        return HttpResponse(simplejson.dumps(f_data))
    elif format == 'xml':
        # TODO add xml serialization capabilities capabilities
        pass
    elif format == 'html':
        from django.template.loader import render_to_string

        return render_to_response("IssueTracker/issue/%s.html" % req, template_args)

@permission_required('IssueTracker.can_view', login_url="/login/")
def viewAllIssues(request, page=1):
    """
    Lists all the Issues 
    """
    setDefaultArgs(request)

    if request.method == "POST":
        data = request.POST
    elif request.method == "GET":
        data = request.GET

    return generateList(data, Issue.objects.filter(resolved_state__isnull=True), page)


def generateList(data, qdict, page):
    """
    Generates a list of issues
    Take some arguments from user in data, the page number to show and the returned query
    items, render out to user
    """

    # TODO need user-defined limits
    num_per_page = data.get('numperpage', 30)

    last_order_by = data.get('orderby', 'last_modified')
    last_order_method = data.get('ometh', 'ASC')


    if last_order_by == 'id':
        order_by = 'issue_id'
    else:
        order_by = last_order_by

    if last_order_method == "ASC":
        order_method = ''
    else:
        order_method = '-'

    issues = qdict.order_by(order_method + order_by)[(page - 1) * 30:page * 30]

    args['issueList'] = issues
    args['last_order_method'] = last_order_method
    args['order'] = order_by

    args['cols'] = {
            'id'            : { 'class': 'r_issue_id', 'order': 'ASC' },
            'title'         : { 'class': 'r_title', 'order': 'ASC' },
            'item'          : { 'class': 'r_item', 'order': 'ASC' },
            'it'            : { 'class': 'r_inv_t', 'order': 'ASC' },
            'group'         : { 'class': 'r_group', 'order': 'ASC' },
            'reporter'      : { 'class': 'r_reporter', 'order': 'ASC' },
            'assignee'      : { 'class': 'r_assignee', 'order': 'ASC' },
            'post_time'     : { 'class': 'r_post_time', 'order': 'ASC' },
            'last_modified' : { 'class': 'r_last_modified', 'order': 'ASC' },
        }

    if args['cols'][last_order_by]['order'] == last_order_method:
        if last_order_method == "ASC":
            args['cols'][last_order_by]['order'] = "DESC"
        else:
            args['cols'][last_order_by]['order'] = "ASC"

    search_term =  data.get('search_term', False)
    args['search_term'] = search_term

    if search_term:
        # kludgy way of doing things
        args['extraArgs'] = '&search_term=%s' % ( search_term )


    return render_to_response("IssueTracker/issue_list.html", args)

