from django.contrib.auth.models import User

from LabtrackerCore.Email import EmailSection
from IssueTracker.Email import NewIssueEmail
import IssueTracker.forms as forms

class IssueUpdater(object):

    def __init__(self, request, issue):
        self.request = request
        self.issue = issue
        self.valid = False

        self.data = request.POST.copy()

        self.updateForm = forms.UpdateIssueForm(self.data, instance=issue)

        # validate and bind form
        if updateIssue.is_valid():
            self.valid = True
            updateIssue.save(commit=False)
        else:
            self.valid = False
            return

        if self.data.has_key('resolved_state') and \
                self.issue.resolved_state != self.updateIssue.resolved_state:
            # FIXME do in form
            updateIssue.resolve_time = datetime.datetime.now()

        if self.data.has_key('comment'):
            self.data.__setitem__('user', str(request.user.id))
            self.data.__setitem__('issue', issue_id)

            self.commentForm = AddCommentForm(self.data)
            if self.commentForm.is_valid():
                self.valid = True
                self.commentForm.save()

            else:
                self.valid = False
                return

        # deal with hooks
        if issue.it:
            hook = utils.issueHooks.getUpdateSubmitHook(issue.it.name)
            if hook:
                if hook(request, issue):
                    self.valid = True
                else:
                    self.valid = False
                    return


    def getEmail(self):
        """
        Create the email, and return it
        """
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

        for user in issue.cc.all():
            issue_email.addCC(user.email)

        return issue_email

    def getUpdateActionString(self):
        """
        Caller is in charge of calling updateHistory on the actionStrings
        """

        if not self.is_valid():
            return None

        curAssignee = self.issue.assignee
        curState = self.issue.resolved_state

        actionStrings = []

        if self.data.has_key('assignee') and \
                (curAssignee != self.updateIssue.assignee):
            actionStrings.append("Assigned to %s" % (updateIssue.assignee))

        if data.has_key('problem_type'):
            # get histmsg from addProblemTypeSection here
            pass

        if data.has_key('resolved_state') and \
                    curState != self.updateIssue.resolved_state:

            actionStrings.append("Changed state to %s" % \
                    (updateIssue.resolved_state))

        #for action in actionStr:
            #utils.updateHistory(request.user, issue, action)
        return actionStrings

    def save(self):
        self.updateIssue.save()

    def is_valid(self):
        return self.valid

