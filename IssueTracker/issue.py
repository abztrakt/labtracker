from django.contrib.auth.models import User

from LabtrackerCore.Email import EmailSection
from IssueTracker.Email import NewIssueEmail
import IssueTracker.forms as forms
import IssueTracker.utils as utils

class IssueUpdater(object):

    def __init__(self, request, issue):
        self.request = request
        self.issue = issue
        self.valid = False

        self.data = request.POST.copy()

        self.updateForm = forms.UpdateIssueForm(self.data, instance=issue)

        # validate and bind form
        if self.updateForm.is_valid():
            self.valid = True
            self.updateForm.save(commit=False)
        else:
            self.valid = False
            raise ValueError("form invalid")

        if self.data.has_key('resolved_state') and \
                self.issue.resolved_state != \
                    self.updateForm.cleaned_data['resolved_state']:
            # FIXME do in form
            self.updateForm.resolve_time = datetime.datetime.now()

        if self.data.has_key('comment'):
            self.data.__setitem__('user', request.user.id)
            self.data.__setitem__('issue', issue.pk)

            self.commentForm = forms.AddCommentForm(self.data)
            if self.commentForm.is_valid():
                self.valid = True
                self.commentForm.save()

            else:
                self.valid = False
                raise ValueError("form invalid")

        # deal with hooks
        if issue.it:
            hook = utils.issueHooks.getUpdateSubmitHook(issue.it.name)
            if hook:
                if hook(request, issue):
                    self.valid = True
                else:
                    self.valid = False
                    raise ValueError("form invalid")

    def getEmail(self):
        """
        Create the email, and return it
        """
        if not self.is_valid():
            raise ValueError("Invalid update, cannot get email")

        issue_email = NewIssueEmail(self.issue)
        curAssignee = self.issue.assignee
        curState = self.issue.resolved_state

        if self.data.has_key('cc'):
            issue_email.addCCSection(self.issue.cc.all().order_by('id'),
                    User.objects.in_bulk(self.data.getlist('cc')).order_by('id'))

        if self.data.has_key('assignee') and \
                (curAssignee != self.updateIssue.assignee):
            issue_email.addAssigneeSection(curAssignee, self.updateIssue.assignee)
            
        if self.data.has_key('problem_type'):
            issue_email.addProblemTypeSection(self.issue.problem_type.all(),
                    self.data.getlist('problem_type'))

        if self.data.has_key('resolved_state') and \
                    curState != self.updateIssue.resolved_state:
            issue_email.addResolveStateSection(updateIssue.resolved_state)

        if self.data.has_key('comment'):
            issue_email.addCommentSection(self.request.user, 
                                          self.data.get('comment'))


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

        curAssignee = self.issue.assignee
        curState = self.issue.resolved_state

        actionStrings = []

        if self.data.has_key('assignee') and \
                (curAssignee != self.updateIssue.assignee):
            actionStrings.append("Assigned to %s" % (updateIssue.assignee))

        if self.data.has_key('problem_type'):
            # get histmsg from addProblemTypeSection here
            pass

        if self.data.has_key('resolved_state') and \
                    curState != self.updateIssue.resolved_state:

            actionStrings.append("Changed state to %s" % \
                    (updateIssue.resolved_state))

        return actionStrings

    def save(self):
        self.updateIssue.save()

    def is_valid(self):
        return self.valid

