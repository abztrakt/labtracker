import datetime
from django.conf import settings
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

        self.valid = True 

        self.data = request.POST.copy()

        self.issue = issue

        self.updateForm = forms.UpdateIssueForm(self.data, instance=issue)
        if self.issue.assignee:
            assigner = self.issue.assignee
        else:
            assigner = None 
        if self.issue.resolved_state:
            resolver= self.issue.resolved_state
        else:
            resolver = None
        if self.issue.cc.all():
            ccers = self.issue.cc.all()
        else:
            ccers = None
        self.old = {
            'cc':       ccers,
            'ptypes':   self.issue.problem_type.all(),
            'assignee': assigner,
            'resolved': resolver,
        }
        import pdb; pdb.set_trace()
        # validate and bind form
        if not self.updateForm.is_valid():
            self.valid = False 
        else:
            self.valid = True 

        self.commentForm = None
        if self.data.has_key('comment'):
            self.data.__setitem__('user', request.user.id)
            self.data.__setitem__('issue', issue.pk)
            self.commentForm = forms.AddCommentForm(self.data)
            if not self.commentForm.is_valid():
                self.valid = False 
        #else:
            #self.commentForm = forms.AddCommentForm()

        # deal with hooks
        self.extraForm = None
        if issue.it:
            hook = utils.issueHooks.getHook("updateForm", issue.it.name)
            if hook:
                self.extraForm = hook(issue, request)
                
                if self.extraForm:
                    if not self.extraForm.is_valid():
                        self.valid = False 

    def getEmail(self):
        """
        Create the email, and return it
        """
        if not self.is_valid():
            raise ValueError("Invalid update, cannot get email")

        issue = im.Issue.objects.get(pk=self.issue_pk)
        issue_email = NewIssueEmail(issue)

        update_data = self.updateForm.cleaned_data
            # need to add the CC users as well
       # if self.data.has_key('cc'):
        #    issue_email.addCCSection(self.old['cc'],
         #          update_data['cc']) 

            # need to add the CC users as well

        if self.data.has_key('assignee') and \
                (self.old['assignee'] !=update_data['assignee']): 
            issue_email.addAssigneeSection(str(self.old['assignee']),
                                           str(update_data['assignee']))
        if self.data.has_key('problem_type'):
            issue_email.addProblemTypeSection(self.old['ptypes'],
                    self.data.getlist('problem_type'))

        if self.data.has_key('resolved_state') and \
                    self.old['resolved'] != update_data['resolved_state']:
            issue_email.addResolveStateSection(update_data['resolved_state'])

        if self.data.has_key('comment'):
            issue_email.addCommentSection(self.request.user, 
                                          self.commentForm.cleaned_data['comment'])
        import pdb; pdb.set_trace() 
        title = self.issue.title
        try:
            title = title.replace('@', '[at]')
        except:
            pass
        issue_email.subject = "[" + settings.EMAIL_SUBJECT_PREFIX + "]" + ' Change to the Issue: %s' % (title)
        if self.data.has_key('cc'):
            for user in update_data['cc']: 
                issue_email.addCC(user.email)

        return issue_email

    def getUpdateActionString(self):
        """
        Caller is in charge of calling updateHistory on the actionStrings
        """

        if not self.is_valid():
            raise ValueError("Invalid update, cannot get action string")
        import pdb; pdb.set_trace()
        update_data = self.updateForm.cleaned_data
        actionStrings = []
        if self.data.has_key('cc') and (str(self.old['cc']) != str(update_data['cc'])):
            old_cc_list = self.old['cc']
            cc_list = update_data['cc']
            cc_list1 = cc_list
            for cc in cc_list:
                count = 0
                count1 = 0
                for old_cc in old_cc_list:
                    count1 = count1+1 
                    if str(old_cc) != str(cc):
                        count = count+1 
                if count ==count1: 
                    actionStrings.append("Added %s to the CC list" % (str(cc)))
            for old_cc in old_cc_list:
                count1 = 1
                for cc in cc_list1:
                    if str(old_cc) == str(cc):
                        count1 =0
                if count1== 1:
                    actionStrings.append("Removed %s to the CC list" % (str(old_cc)))


        if self.data.has_key('assignee')and \
               (self.old['assignee'] != update_data['assignee']):
            actionStrings.append("Assigned to %s" % (update_data['assignee']))

        if self.data.has_key('problem_type') and (str(self.old['ptypes']) != str(update_data['problem_type'])):
            old_problems = self.old['ptypes']
            problems = update_data['problem_type']
            problems1 = problems
            for problem in problems:
                count = 0
                count1 = 0
                for old_problem in old_problems:
                    count1 = count1+1 
                    if str(old_problem) != str(problem):
                        count = count+1 
                if count ==count1: 
                    actionStrings.append("Added the problem type %s" % (str(problem)))
            for old_problem in old_problems:
                count1 = 1
                for p in problems1:
                    if str(old_problem) == str(p):
                        count1 =0
                if count1== 1:
                    actionStrings.append("Removed the problem type %s" % (str(old_problem)))

        if self.data.has_key('resolved_state') and \
                    self.old['resolved']!= update_data['resolved_state']:

            actionStrings.append("Changed state to %s" % \
                    (update_data['resolved_state']))

        return actionStrings

    def save(self):
         if self.commentForm:
            if self.commentForm.is_valid():
                self.commentForm.save()
                self.updateForm.save()

                if self.extraForm:
                    if self.extraForm.is_valid():
                        self.extraForm.save()

    def is_valid(self):
        return self.valid

