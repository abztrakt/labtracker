from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django import newforms as forms
from django.newforms import form_for_model
from django.shortcuts import render_to_response, get_object_or_404

import simplejson
from django.core import serializers

from labtracker.IssueTracker.models import *
import labtracker.LabtrackerCore.models as LabtrackerCore
from labtracker.IssueTracker.forms import *

args = { 'loggedIn' : False, }

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

    # need to get app root somehow
    roadmap = open('/var/www/django_apps/labtracker/DOCUMENTATION/roadmap')
    args['roadmap'] = roadmap.read()
    roadmap.close()

    readme = open('/var/www/django_apps/labtracker/DOCUMENTATION/README')
    args['readme'] = readme.read()
    readme.close()

    return render_to_response('IssueTracker/index.html', args)

def post(request, issue_id):
    """
    This is for posting comments, and modifying some things for issues after they are
    created.
    Requires a post request, otherwise nothing is done.
    """
    issue = get_object_or_404(Issue, pk=issue_id)
    UpdateIssueForm = forms.form_for_instance(issue, 
            fields=('issue_id','assignee','cc','resolve_time', 'resolved_state', 
                'last_modified'))

    if request.method == 'POST':
        actionStr = ""
        curAssignee = issue.assignee
        curState = issue.resolved_state
        data = request.POST.copy()

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
            actionStr += "<li>Assigned to %s</li>" % (updateIssue.assignee)
        if data.has_key('resolved_state') and not (curState == updateIssue.resolved_state):
            actionStr += "<li>Changed state to %s</li>" % (updateIssue.resolved_state)

        if (actionStr):
            updateIssue.save()
            # also will need to create a new IssueHistory item
            history = IssueHistory(user=request.user,change=actionStr,issue=issue)
            history.save()

        if data.has_key('comment') and (not (data['comment'] in ("", None))):
            data['user'] = str(request.user.id)
            data['issue'] = issue_id

            newComment = AddCommentForm(data)
            if newComment.is_valid():
                newComment = newComment.save()
            else:
                args['add_comment_form'] = newComment
                print "Form not valid"
                print newComment.errors
                #args['comment_errors'] = newComment.errors
    else:
        return Http404()

    return HttpResponseRedirect(reverse('view', args=[issue.issue_id]))

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
        postResp['status'] = 1
    elif data['action'] == "addcc":
        user = get_object_or_404(User, username=data['user'])
        issue.cc.add(user)
        postResp['username'] = user.username
        postResp['userid'] = user.id
        postResp['status'] = 1

    # FIXME: Needs to deal with error handling here, what happens when user could not have
    # been removed?

    if request.method == "POST":
        # POST means an ajax call and so will do a json response
        return HttpResponse(simplejson.dumps(postResp))
    elif request.method == "GET":
        # direct call, will need to redirect
        return HttpResponseRedirect(reverse('view', args=[issue.issue_id]))
modIssue = permission_required('IssueTracker.add_issue')(modIssue)

def view(request, issue_id):
    """
    This is called when the issue requests a specific issue.
    Basically displays the requested issue and any related comments. Offers the
    user the ability to add comments to the issue.
    If a post is given, will also post a comment
    """
    setDefaultArgs(request)

    # get the issue
    issue = get_object_or_404(Issue, pk=issue_id)
    UpdateIssueForm = forms.form_for_instance(issue, 
            fields=('issue_id','assignee','cc','resolve_time', 'resolved_state', 
                'last_modified'))


    args['issue'] = issue
    args['history'] = IssueHistory.objects.filter(issue=issue).order_by('time')
    args['comments'] = IssuePost.objects.filter(issue=issue).order_by('post_date')

    args['add_comment_form'] = AddCommentForm()
    args['update_issue_form'] = UpdateIssueForm()

    return render_to_response('IssueTracker/view.html', args)
view = permission_required('IssueTracker.can_view')(view)

def reportList(request):
    """
    Currently does nothing but will list out all the available queries to list available
    reports
    """
    setDefaultArgs(request)
    return render_to_response('IssueTracker/list.html', args)
reportList = permission_required('IssueTracker.can_view')(reportList)

def report(request, report_id):
    """
    View a specific report
    """
    setDefaultArgs(request)
    return render_to_response('IssueTracker/report.html', args)
report = permission_required('IssueTracker.can_view')(report)

def user(request):
    """
    User preference pane, may be renamed later
    """
    setDefaultArgs(request)
    return render_to_response('IssueTracker/user.html', args)
user = login_required(user)

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
            print form.errors
            print "Form was not valid"

    form = CreateIssueForm()
    args['form'] = form
    return render_to_response('IssueTracker/create.html', args)
createIssue = permission_required('IssueTracker.add_issue')(createIssue)


###################
# JSON Generators #

def getGroups(request, it_type):
    """
    Given an inventory type, will return a list of groups that belongs to that
    inventory_type
    """
    import labtracker.Machine.models as Machine
    query = Machine.Group.objects.filter(group__it=it_type)

    json_serializer = serializers.get_serializer("json")()
    return HttpResponse('{"groups":%s}' % (json_serializer.serialize(query)))
getGroups = permission_required('IssueTracker.add_issue')(getGroups)

def getItems(request, group_id):
    """
    Given an inventory type, will return a list of groups that belongs to that
    inventory_type
    """
    import labtracker.Machine.models as Machine
    query = Machine.Group.objects.get(pk=group_id).machines.all() #.machine_set.all()
    print query

    json_serializer = serializers.get_serializer("json")()
    return HttpResponse('{"items":%s}' % (json_serializer.serialize(query)))
getItems = permission_required('IssueTracker.add_issue')(getItems)
