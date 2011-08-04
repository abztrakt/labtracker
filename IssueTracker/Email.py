from LabtrackerCore.Email import Email, EmailSection
from django.template.loader import render_to_string
from django.conf import settings
import models

class NewIssueEmail(Email):

    def __init__(self, issue, title=None, *args, **kwargs):
        try:
            title = title.replace('@', '[at]')
        except:
            pass

        kwargs['subject'] = "[" + settings.EMAIL_SUBJECT_PREFIX + "]" + " #%d: %s " % (issue.pk, title)

        super(NewIssueEmail, self).__init__(sections=[], *args, **kwargs)

        self.issue = issue

        if title:
            self.appendSection(EmailSection(title))
        else:
            self.appendSection(
                    EmailSection("[Issue %d]" % (issue.pk)))


    def addCCSection(self, old_cc, new_cc):
        """
        handle the cc updating for an issue
        """
        # CC is special in that it only updates this area
        if old_cc:
            curUsers = set(str(user) for user in old_cc)
        else:
            curUsers = set()
        if new_cc:
            newUsers = set(str(user) for user in new_cc)
        else:
            newUsers = set()
        # get
        removeCC = curUsers.difference(newUsers)
        removeList = ", ".join(removeCC) 
        if removeCC:
            removeSection = EmailSection("Users removed from CC list")
            removeSection.content = "%s" % (removeList)
            self.appendSection(removeSection)

        # now curUsers only contains the users that need not be modified
        # add all newUsers not in curUser to cc list
        addCC = newUsers.difference(curUsers)
        addList = ", ".join(addCC)
        if addCC:
            addSection = EmailSection("Users added to CC list")
            addSection.content = "%s" % (addList) 
            self.appendSection(addSection)

    def addAssigneeSection(self, cur, new):
        assigneeSection = EmailSection("Assignee Change")
        if cur != None:
            assigneeSection.content = "Reassigned from %s to %s." % (cur, new)
        else:
            assigneeSection.content = new
        self.appendSection(assigneeSection)

    def addProblemTypeSection(self, cur_ptypes, new_ptypes):
        """
        Update an issue's problem types
        """
        # XXX addProblemTypeSection shouldn't return a hist_msg
        given_pt = {}

        # cur_ptypes is given as objects
        # new_ptypes is given as pk
        cur_ptypes = set([str(ptype.pk) for ptype in cur_ptypes])
        new_ptypes = set(new_ptypes)

        # Any problem type that is not given, will need to be marked for removal
        remove = cur_ptypes.difference(new_ptypes)
        add = new_ptypes.difference(cur_ptypes)

        drop_items = [models.ProblemType.objects.get(pk=ii).name for ii in remove]
        add_items = [models.ProblemType.objects.get(pk=ii).name for ii in add]

        hist_msg = ""
        if add_items:
            message = render_to_string('email/email_problemtype.txt', { "problem_type": add_items })
            header = "New Problem Types"
            
            """
            # FIXME use a template
            self.appendSection(EmailSection(
                "New Problem Types", ", ".join(add_items)
            ))

            hist_msg += "<span class='label'>Added problems</span>: %s" \
                    % (", ".join(add_items))
            """
            self.appendSection(EmailSection(header, message))

        if drop_items:
            message = render_to_string('email/email_problemtype.txt', { "problem_type": drop_items })
            hist_msg += "<br />"
            header = "Removed Problem Types"

            """
            # FIXME use a template
            self.appendSection(EmailSection(
                "Removed Problem Types", ", ".join(drop_items)
            ))

            hist_msg += "<span class='label'>Removed problems</span>: %s" \
                    % (", ".join(drop_items))
            """

            self.appendSection(EmailSection(header, message))
        return hist_msg


    def addResolveStateSection(self, state):
        """
        """
        curState = self.issue.resolved_state

        if curState == state:
            return

        resolveSection = EmailSection("Issue Resolve State")

        # FIXME use a template
        resolveSection.content = "Resolved from %s to %s." % (curState, state)
        self.appendSection(resolveSection)

    def addCommentSection(self, user, comment):
        """
        """
        if user:
            self.appendSection(EmailSection(
                "Comment from %s" % (user.username), comment))
        else:
            self.appendSection(EmailSection(comment))
