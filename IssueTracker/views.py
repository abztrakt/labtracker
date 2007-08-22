from labtracker.IssueTracker.models import *
from django.conf.urls.defaults import *
from labtracker.IssueTracker.forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django import newforms as forms
from django.newforms import form_for_model


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
    return render_to_response('IssueTracker/index.html', args)

def create(request):
    """
    This is the view called when the user is creating a new issue, not for 
    posting comments.
    Currently takes a request, and sets the reporter to whoever is logged in and
    then saves it.
    """
    # TODO improve the form validation here
    # FIXME need to add the ability to choose Group and Item 
    setDefaultArgs(request)
    if request.method == 'POST':
        data = request.POST.copy()          # need to do this to set some defaults
        data['reporter'] = str(request.user.id)
        form = CreateIssueForm(data)
        if form.is_valid():
            issue = form.save()
        else:
            print form.errors
            print "Form was not valid"
    else:
        print "Not a post method"
        form = CreateIssueForm()
        args['form'] = form
    return render_to_response('IssueTracker/create.html', args)
create = permission_required('IssueTracker.add_issue')(create)

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

    if request.method == 'POST':
        actionStr = ""
        curAssignee = issue.assignee
        curState = issue.resolved_state
        updateIssue = UpdateIssueForm(request.POST)
        updateIssue = updateIssue.save(commit=False)
        if not (curAssignee == updateIssue.assignee):
            actionStr += "<li>Assigned to %s</li>" % (updateIssue.assignee)
        if not (curState == updateIssue.resolved_state):
            actionStr += "<li>Changed state to %s</li>" % (updateIssue.resolved_state)

        if (actionStr):
            # TODO the current way this work sucks, should keep track at a mroe granular level
            updateIssue.save()
            # also will need to create a new IssueHistory item
            history = IssueHistory(user=request.user,change=actionStr,issue=issue)
            history.save()

        data = request.POST.copy()
        if (not (data['comment'] in ("", None))):
            data['user'] = str(request.user.id)
            data['issue'] = issue_id

            # TODO will need to also strip all html at this point from the comment
            print data['comment']
            newComment = AddCommentForm(data)
            if newComment.is_valid():
                newComment = newComment.save()
            else:
                args['add_comment_form'] = newComment
                print "Form not valid"
                print newComment.errors
                #args['comment_errors'] = newComment.errors
    else:
        args['add_comment_form'] = AddCommentForm()
        args['update_issue_form'] = UpdateIssueForm()

    args['issue'] = issue
    args['history'] = IssueHistory.objects.filter(issue=issue).order_by('time')

    # TODO need to make sure that this is being sorted by date
    args['comments'] = IssuePost.objects.filter(issue=issue).order_by('post_date')

    return render_to_response('IssueTracker/view.html', args)
view = permission_required('IssueTracker.can_view')(view)

def allIssues(request):
    """
    Currently, all this does is grab a list of issues from the db and dumps it
    to template
    """
    setDefaultArgs(request)
    issueList = Issue.objects.all().order_by('-last_modified')
    args['issueList'] = issueList
    return render_to_response('IssueTracker/all.html', args)
allIssues = permission_required('IssueTracker.can_view')(allIssues)

def reportList(request):
    setDefaultArgs(request)
    return render_to_response('IssueTracker/list.html', args)
reportList = permission_required('IssueTracker.can_view')(reportList)

def report(request, report_id):
    setDefaultArgs(request)
    return render_to_response('IssueTracker/report.html', args)
report = permission_required('IssueTracker.can_view')(report)

def user(request):
    setDefaultArgs(request)
    return render_to_response('IssueTracker/user.html', args)
user = login_required(user)
