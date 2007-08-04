# Create your views here.
from labtracker.IssueTracker.models import *
from labtracker.IssueTracker.create import *
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django import newforms as forms

args = { 'loggedIn' : False, }

def setDefaultArgs(request):
    #args['loggedIn'] = request.user.is_authenticated()
    args['user'] = request.user

def index(request):
    """
    Used for log in as well
    """
    setDefaultArgs(request)
    return render_to_response('IssueTracker/index.html', args)

def create(request):
    setDefaultArgs(request)
    return render_to_response('IssueTracker/create.html', args)
create = permission_required('IssueTracker.add_issue')(create)

def view(request, issue_id):
    setDefaultArgs(request)
    return render_to_response('IssueTracker/view.html', args)
view = permission_required('IssueTracker.can_view')(view)

def post(request, issue_id):
    setDefaultArgs(request)
    return render_to_response('IssueTracker/post.html', args)
post = permission_required('IssueTracker.add_issuepost')(post)

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
