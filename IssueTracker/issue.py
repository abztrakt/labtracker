import datetime

from django.contrib.auth.models import User

from LabtrackerCore.Email import EmailSection
from Email import NewIssueEmail
import models as im
import forms
import utils

class IssueUpdater(object):

    def __init__(self, request, issue):
        self.request = request
        self.issue_pk = issue.pk

        self.valid = False

        self.data = request.POST.copy()

        self.issue = issue

        self.updateForm = forms.UpdateIssueForm(self.data, instance=issue)

        self.old = {
            'cc':       issue.cc.all().order_by('id'),
            'ptypes':   self.issue.problem_type.all()
        }

        # validate and bind form
        if self.updateForm.is_valid():
            self.valid = True
        else:
            self.valid = False

        if self.data.has_key('comment'):
            self.data.__setitem__('user', request.user.id)
            self.data.__setitem__('issue', issue.pk)

            self.commentForm = forms.AddCommentForm(self.data)
            if self.commentForm.is_valid():
                self.valid = True
            else:
                self.valid = False

        # deal with hooks
        self.extraForm = None
        if issue.it:
            hook = utils.issueHooks.getHook("updateForm", issue.it.name)
            if hook:
                self.extraForm = hook(issue, request)
                self.has_hook = True

                if self.extraForm.is_valid():
                    self.valid = True
                else:
                    self.valid = False
            else:
                self.has_hook = False

    def getEmail(self):
        """
        Create the email, and return it
        """
        if not self.is_valid():
            raise ValueError("Invalid update, cannot get email")

        issue = im.Issue.objects.get(pk=self.issue_pk)
        issue_email = NewIssueEmail(issue)

        update_data = self.updateForm.cleaned_data

        if self.data.has_key('cc'):
            issue_email.addCCSection(self.old['cc'],
                    User.objects.in_bulk(self.data.getlist('cc')).order_by('id'))

            # need to add the CC users as well

        if self.data.has_key('assignee') and \
                (self.issue.assignee != update_data['assignee']):
            issue_email.addAssigneeSection(self.issue.assignee, update_data['assignee'])
            
        if self.data.has_key('problem_type'):
            issue_email.addProblemTypeSection(self.old['ptypes'],
                    self.data.getlist('problem_type'))

        if self.data.has_key('resolved_state') and \
                    self.issue.resolved_state != update_data['resolved_state']:
            issue_email.addResolveStateSection(update_data['resolved_state'])

        if self.data.has_key('comment'):
            issue_email.addCommentSection(self.request.user, 
                                          self.commentForm.cleaned_data['comment'])


        issue_email.subject = '[labtracker] %s' % (self.issue.title)

        for user in self.issue.cc.all():
            issue_email.addCC(user.email)

        return issue_email

    def getUpdateActionString(self):
        """
        Caller is in charge of calling updateHistory on the actionStrings
        """

        if not self.is_valid():
            raise ValueError("Invalid update, cannot get action string")

        update_data = self.updateForm.cleaned_data

        actionStrings = []

        if self.data.has_key('assignee') and \
                (self.issue.assignee != update_data['assignee']):
            actionStrings.append("Assigned to %s" % (update_data['assignee']))

        if self.data.has_key('problem_type'):
            # get histmsg from addProblemTypeSection here
            pass

        if self.data.has_key('resolved_state') and \
                    self.issue.resolved_state != update_data['resolved_state']:

            actionStrings.append("Changed state to %s" % \
                    (update_data['resolved_state']))

        return actionStrings

    def save(self):
        self.updateForm.save()
        if self.data.has_key('comment'):
            self.commentForm.save()

    def is_valid(self):
        return self.valid

