from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse, \
        HttpResponseServerError
from django import newforms as forms
from django.newforms import form_for_model
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.list_detail import object_list
from django.contrib.auth.models import User
import django.db.models.loading as load

import simplejson
from django.core import serializers

from labtracker.IssueTracker.models import *
import labtracker.LabtrackerCore.models as LabtrackerCore
from labtracker.IssueTracker.forms import *
import labtracker.IssueTracker.search as issueSearch

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
    todos = open('/var/www/django_apps/labtracker/DOCUMENTATION/TODO')
    args['todos'] = todos.read()
    todos.close()

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

def search(request):
    """
    Takes a post, searches, and either redirects to a list of matching items (or no
    items), or the specific issue
    """
    setDefaultArgs(request)
    extra_context = {}

    if request.method == 'POST':
        # in this case, we get to process the stuff
        data = request.POST.copy()
        try:
            issue_id = int(data['search_term'])
        except ValueError, e:
            issues = Issue.objects.filter(title__contains=data['search_term'])
            print issues
            return HttpResponse(object_list(request, queryset=issues, 
                extra_context = extra_context, allow_empty=True))
        except Exception, e:
            # other exceptions
            return HttpResponseServerError

        extra_context['error'] = 'Issue with id "%i" not found.' % issue_id
        extra_context['search_by_id'] = True

        try:
            issue = Issue.objects.get(pk=issue_id)
            return HttpResponseRedirect(reverse('view', args=[issue.issue_id]))
        except ObjectDoesNotExist, e:
            issues = Issue.objects.filter(title__contains=data['search_term'])
            print issues

            return HttpResponse(object_list(request, queryset=issues, 
                extra_context = extra_context, allow_empty=True))
        except Exception, e:
            # other exceptions
            return HttpResponseServerError()

    else:
        return HttpResponseRedirect(reverse('index'))
search = permission_required('IssueTracker.can_view')(search)

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
            print 'getting search list'
            searches = issueSearch.parseSearch(data)
            print 'passing list to query'
            query = issueSearch.buildQuery(searches)

            extra_context = {}

            return HttpResponse(object_list(request, queryset=query, 
                extra_context = extra_context, allow_empty=True))


    args['add_query'] = AddSearchForm()

    return render_to_response('IssueTracker/adv_search.html', args)
advSearch = permission_required('IssueTracker.can_view')(advSearch)

###################
# ajax generators #

def getSearchField(request, field_name):
    """ 
    Retrieves a search field and returns it in JSON

    """
    field = issueSearch.searchFieldGen(field_name)

    # TODO some better escaping needs to be done
    return HttpResponse("{ 'label': '%s', 'field': '%s' }" % \
            (field.label, field.widget.render(field_name, "").replace("\n", "")))
getSearchField = permission_required('IssueTracker.add_issue')(getSearchField)
    
def getGroups(request, it_type):
    """
    Given an inventory type, will return a list of groups that belongs to that
    inventory_type
    """
    # get namespace
    inv_type = LabtrackerCore.InventoryType.objects.get(pk=it_type)
    print inv_type.namespace

    # now grab the model

    ac = load.AppCache()
    model = ac.get_model(inv_type.namespace, 'Group')

    #query = Machine.Group.objects.filter(group__it=it_type)
    query = model.objects.all()

    json_serializer = serializers.get_serializer("json")()
    return HttpResponse('{"groups":%s}' % (json_serializer.serialize(query)))
getGroups = permission_required('IssueTracker.add_issue')(getGroups)

def getItems(request, group_id):
    """
    Given an inventory type, will return a list of groups that belongs to that
    inventory_type
    """
    inv_type = LabtrackerCore.Group.objects.get(pk=group_id).it

    ac = load.AppCache()
    model = ac.get_model(inv_type.namespace, 'Group')
    query = model.objects.get(pk=group_id).machines.all() 

    json_serializer = serializers.get_serializer("json")()
    return HttpResponse('{"items":%s}' % (json_serializer.serialize(query)))
getItems = permission_required('IssueTracker.add_issue')(getItems)
