import datetime

import simplejson

from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, \
        HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from IssueTracker.models import *
from IssueTracker.issue import IssueUpdater
import LabtrackerCore.models as cModels
from IssueTracker.forms import *
import IssueTracker.utils as utils


@permission_required('IssueTracker.add_issue', login_url="/login/")
def modIssue(request, issue_id):
    """
    Can be accessed through post or get, will redirect immediately afterwards
    """
    issue = get_object_or_404(Issue, pk=issue_id)
    postResp = {}

    data = request.POST.copy()

    action = data.get('action')
    if action == "dropcc":
        user = get_object_or_404(User, pk=int(data['user']))
        issue.cc.remove(user)
        utils.updateHistory(request.user, issue, "Removed %s from CC list" % (user))
        postResp['status'] = 1
    elif action == "addcc":
        user = get_object_or_404(User, username=data['user'])
        issue.cc.add(user)
        utils.updateHistory(request.user, issue, "Added %s to CC list" % (user))
        postResp['username'] = user.username
        postResp['userid'] = user.id
        postResp['status'] = 1

    # FIXME: Needs to deal with error handling here, what happens when user 
    # could not have been removed?

    if request.is_ajax():
        # means an ajax call and so will do a json response
        return HttpResponse(simplejson.dumps(postResp))
    else:
        # direct call, will need to redirect
        return HttpResponseRedirect(reverse('IssueTracker-view', 
                                            args=[issue.issue_id]))

@permission_required('IssueTracker.can_view', login_url="/login/")
def viewIssue(request, issue_id):
    """
    This is called when the issue requests a specific issue.
    Basically displays the requested issue and any related comments. Offers the
    user the ability to add comments to the issue.
    If a post is given, will also post a comment
    """

    # get the issue
    issue = get_object_or_404(Issue, pk=issue_id)

    args = {
            'issue': issue,
            'history': IssueHistory.objects.filter(issue=issue).order_by('-time'),
            'comments': IssueComment.objects.filter(issue=issue).order_by('time')
        }
    extraForm = None

    if request.method == 'POST':
        issueProcessor = IssueUpdater(request, issue)
       #CHANGE 
        # if everything passed, redirect to self
        if issueProcessor.is_valid():
            email = issueProcessor.getEmail()
            issueProcessor.save() 
            email.send()
            for action in issueProcessor.getUpdateActionString():
                utils.updateHistory(request.user, issue, action)

            return HttpResponseRedirect(reverse('IssueTracker-view', args=[issue.issue_id]))
        form = issueProcessor.updateForm
        commentForm = issueProcessor.commentForm or AddCommentForm()
        extraForm = issueProcessor.extraForm
    else:
        form = UpdateIssueForm(instance=issue)
        commentForm = AddCommentForm()
        if issue.it:
            hook = utils.issueHooks.getHook("updateForm", issue.it.name)
            if hook:
                extraForm = hook(issue)

    #CHANGE
    args['add_comment_form'] = commentForm
    args['update_issue_form'] = form
    args['problem_types'] = form.fields['problem_type'].queryset
    args['extra_form'] = extraForm
    #CHANGE
    args['valid_form']= commentForm.is_valid()

    return render_to_response('view.html', args,
            context_instance=RequestContext(request))

@permission_required('IssueTracker.add_issue', login_url="/login/")
def createIssue(request):
    """
    This is the view called when the user is creating a new issue, not for 
    posting comments.
    Currently takes a request, and sets the reporter to whoever is logged in and
    then saves it.
    """

    if request.method == 'POST':
        data = request.POST.copy()          # need to do this to set some defaults
        data['reporter'] = str(request.user.id)

        form = CreateIssueForm(data)
        if form.is_valid():
            inv_t = form.cleaned_data['it']

            # need to call hook now and see if it is good
            hook = utils.issueHooks.getCreateSubmitHook(inv_t.name)

            if hook:
                # need to get the item or group here
                group = form.cleaned_data['group']

                item = None
                if form.cleaned_data['item']:
                    item = form.cleaned_data['item'].item

                valid = hook(request, item=item, group=group)
            else:
                valid = True

            if valid:
                issue = form.save()
                return HttpResponseRedirect(reverse('IssueTracker-view', \
                        args=[issue.issue_id]))
            
        else:
            # form was not valid, errors should be on form though, so nothing
            # needs to be done
            pass
    else:
        form = CreateIssueForm()

    form.fields['item'].queryset = form.fields['item'].queryset.order_by('it', 'name')

    args = {
        'form': form,
        'problem_types': form.fields['problem_type'].queryset
    }

    return render_to_response('create.html', args,
            context_instance=RequestContext(request))

@permission_required('IssueTracker.can_view', login_url="/login/")
def history(request, item_id, page=1):
    """
    Given an item, will look up the history for the item
    """
    item = get_object_or_404(cModels.Item, pk=item_id)

    # with the item, we can look up all the history that the item has had
    issues = Issue.objects.filter(item=item_id).\
            order_by('-post_time', 'last_modified')

    args = { 'item': item, 'history': issues }

    return render_to_response('history.html', args,
            context_instance=RequestContext(request))

@permission_required('IssueTracker.can_view', login_url="/login/")
def fetch(request, issue_id): #TODO move this to ajax.py
    """
    Fetch information for a given issue
    Needs request params:
        req     -- What data is being requested
        format  -- What format data should be returned in
    """
    issue = get_object_or_404(Issue, pk=issue_id)

    data = request.GET.copy()

    if not data.has_key('req'):
        return HttpResponseNotFound()

    req = data.get('req')
    format = data.get('format', 'json')
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

    if req == 'cclist':
        return render_to_response('cc_list.html', {'issue':issue})
               

    if format == 'json':
        # for security reasons, send hash not list
        f_data = {}
        for piece in req_data:
            f_data[piece[pk]] = piece
        return HttpResponse(simplejson.dumps(f_data))
    elif format == 'xml':
        # TODO add xml serialization capabilities 
        pass
    elif format == 'html':
        return render_to_response("issue/%s.html" % req, template_args,
                context_instance=RequestContext(request))
    else:
        return HttpResponseServerError("Unknown data fromat")

