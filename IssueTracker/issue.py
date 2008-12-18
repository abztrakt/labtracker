from django.contrib.auth.models import User

import LabtrackerCore.Email as Email
import IssueTracker.forms as forms

def updateIssueCC(issue, cc_list, email=None):
    """
    handle the cc updating for an issue
    """
    # CC is special in that it only updates this area
    newUsers = set(User.objects.in_bulk(cc_list).order_by('id'))
    curUsers = set(issue.cc.all().order_by('id'))

    removeCC = []
    # find items that need to be removed
    # FIXME this is terrible inefficient, would be better if the 
    #   newUsers list is shortened

    # find curUsers not in newUsers, remove them
    for user in curUsers.difference(newUsers):
        if curUser not in newUsers:
            removeCC.append(curUser)
            issue.cc.remove(curUser)

    if removeCC and email:
        email.appendSection(Email.EmailSection(
            "Users removed from CC",
            ", ".join(removeCC)
        ))

    addCC = []
    # now curUsers only contains the users that need not be modified
    # add all newUsers not in curUser to cc list
    for user in newUsers.difference(curUsers):
        addCC.append(newUser)
        issue.cc.add(newUser)

    if addCC and email:
        issue_email.appendSection(Email.EmailSection(
            "Users removed from CC", ", ".join(addCC)
        ))

def updateIssueProblemTypes(issue, ptypes, email=None):
    """
    Update an issue's problem types
    """
    given_pt = {}

    # for each one that has been sent in args
    for g_pt in ptypes:
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
        # FIXME use a template
        email.appendSection(Email.EmailSection(
            "New Problem Types", ", ".join(add_items)
        ))

        hist_msg += "<span class='label'>Added problems</span>: %s" \
                % (", ".join(add_items))

        if drop_items:
            hist_msg += "<br />"

    if drop_items:
        # FIXME use a template
        email.appendSection(Email.EmailSection(
            "Removed Problem Types", ", ".join(drop_items)
        ))

        hist_msg += "<span class='label'>Removed problems</span>: %s" \
                % (", ".join(drop_items))

    if hist_msg:
        utils.updateHistory(request.user, issue, hist_msg)


def processIssueUpdate(request, issue):
    """
    This is for posting comments, and modifying some things for issues after 
    they are created.
    Requires a post request, otherwise nothing is done.
    """
    actionStr = []
    curAssignee = issue.assignee
    curState = issue.resolved_state
    data = request.POST.copy()

    updateIssue = forms.UpdateIssueForm(data, instance=issue)
    updateIssue = updateIssue.save(commit=False)

    issue_email = Email.Email()

    issue_email.appendSection(
            Email.EmailSection("[Issue %d updates]" % (issue.pk)))

    if data.has_key('cc'):
        updateIssueCC(issue, data.getlist('cc'), email=issue_email)

    if data.has_key('assignee') and not (curAssignee == updateIssue.assignee):

        assigneeSection = Email.EmailSection("Assignee Change")
        if curAssignee != None:
            assigneeSection.content = "%s ----> %s" % (curAssignee, 
                    updateIssue.assignee)
        else:
            assigneeSection.content = updateIssue.assignee
        issue_email.appendSection(assigneeSection)

        actionStr.append("Assigned to %s" % (updateIssue.assignee))

    if data.has_key('problem_type'):
        updateIssueProblemTypes(issue, data.getlist('problem_type'), 
                                email=issue_email)
        
    if data.has_key('resolved_state') and 
            (curState != updateIssue.resolved_state):

        updateIssue.resolve_time = datetime.datetime.now()

        resolveSection = Email.EmailSection("Issue Resolve State")

        # FIXME use a template
        if curState != None:
            resolveSection.content = "%s ---> %s" % (curState,\
                                                     updateIssue.resolved_state)
        else:
            resolveSection.content = updateIssue.resolved_state
        issue_email.appendSection(resolveSection)

        actionStr.append("Changed state to %s" % \
                (updateIssue.resolved_state))

    if (actionStr):
        updateIssue.save()
        for action in actionStr:
            utils.updateHistory(request.user, issue, action)

    if data.has_key('comment'):
        data['user'] = str(request.user.id)
        data['issue'] = issue_id

        newComment = AddCommentForm(data)
        if newComment.is_valid():
            newComment = newComment.save()

            issue_email.appendSection(Email.EmailSection(
                "Comment from %s" % (request.user.username), 
                data['comment']
            ))
        else:
            pass
            # Form not valid
            #args['add_comment_form'] = newComment
    
    # deal with hooks
    if issue.it:
        hook = utils.issueHooks.getUpdateSubmitHook(issue.it.name)
        if not hook(request, issue):
            return Http404()

    # Send issue_email

    if not issue_email.empty():
        # get the cc list
        cc_list = issue.cc.all()

        issue_email.subject = '[labtracker] %s' % (issue.title)

        for user in cc_list:
            issue_email.addCC(user.email)

        issue_email.send()

    else:
        return Http404()

