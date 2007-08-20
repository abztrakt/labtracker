from labtracker.IssueTracker.models import *
from django.conf.urls.defaults import *
from labtracker.IssueTracker.forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django import newforms as forms


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
    """
    setDefaultArgs(request)
    # get the issue
    issue = get_object_or_404(Issue, pk=issue_id)
    args['issue'] = issue

    # TODO need to make sure that this is being sorted by date
    args['comments'] = IssuePost.objects.filter(issue=issue)

    # get the forms
    args['add_comment_form'] = AddCommentForm()
    args['update_issue_form'] = UpdateIssueForm()
    return render_to_response('IssueTracker/view.html', args)
view = permission_required('IssueTracker.can_view')(view)

def post(request, issue_id):
    """
    This is for the posting of comments to issues, it is also used to update
    issues states and assignee
    """
    issue_id = int(issue_id)
    print "post called with %d" % (issue_id)
    setDefaultArgs(request)
    if request.method == 'POST':
        issue = get_object_or_404(Issue, pk=issue_id)
        newComment = AddCommentForm(request.POST)
        updateIssue = UpdateIssueForm(request.POST)

        #fields=('issue_id','assignee','cc','resolve_time',
                #'resolved_state', 'last_modified')
        updateIssue = updateIssue.save(commit=False)
        if (updateIssue.assignee is not None):
            issue.assignee = updateIssue.assignee
        if (updateIssue.resolved_state is not None):
            issue.resolved_state = updateIssue.resolved_state
        issue.save()

        print type(newComment)
        newComment = newComment.save(commit=False)
        newComment.issue = issue
        newComment.user = request.user
        #newComment.save()

        #if obj.is_valid():
            #issue = obj.save()
        #else:
            #print form.errors
            #print "Form was not valid"

        return HttpResponseRedirect('/issue/%i/' % (issue_id))
    else:
        raise Http404

    return render_to_response('IssueTracker/post.html', args)
post = permission_required('IssueTracker.add_issuepost')(post)

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
