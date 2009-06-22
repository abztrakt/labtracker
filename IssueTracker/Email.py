from LabtrackerCore.Email import Email, EmailSection
from django.template.loader import render_to_string
import models

class NewIssueEmail(Email):

    def __init__(self, issue, *args, **kwargs):
        kwargs['subject'] = "[Issue %d updates]" % (issue.pk)

        super(NewIssueEmail, self).__init__(*args, **kwargs)

        self.issue = issue

        self.appendSection(
                EmailSection("[Issue %d updates]" % (issue.pk)))


    def addCCSection(self, old_cc, new_cc):
        """
        handle the cc updating for an issue
        """
        # CC is special in that it only updates this area
        curUsers = set(old_cc)
        newUsers = set(new_cc)

        # get
        removeCC = curUsers.difference(newUsers)
        if removeCC:
            self.appendSection(Email.EmailSection(
                "Users removed from CC",
                ", ".join(removeCC)
            ))

        # now curUsers only contains the users that need not be modified
        # add all newUsers not in curUser to cc list
        addCC = newUsers.difference(curUsers)
        if addCC:
            self.appendSection(Email.EmailSection(
                "Users added to CC", ", ".join(addCC)
            ))


    def addAssigneeSection(self, cur, new):
        assigneeSection = EmailSection("Assignee Change")
        if cur != None:
            assigneeSection.content = "%s ----> %s" % (cur, new)
        else:
            assigneeSection.content = new
        self.appendSection(assigneeSection)

    def addProblemTypeSection(self, cur_ptypes, new_ptypes):
        """
        Update an issue's problem types
        """
        # XXX addProblemTypeSection shouldn't return a hist_msg
        given_pt = {}

        cur_ptypes = set(cur_ptypes)
        new_ptypes = set(new_ptypes)

        # Any problem type that is not given, will need to be marked for removal
        remove = cur_ptypes.difference(new_ptypes)
        add = new_ptypes.difference(cur_ptypes)

        drop_items = [models.ProblemType.objects.get(pk=ii.pk).name for ii in remove]
        add_items = [models.ProblemType.objects.get(pk=ii).name for ii in add]

        hist_msg = ""
        if add_items:
            message = render_to_string('email/email_problemtype.html', { "problem_type": add_items })
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
                hist_msg += "<br />"

        if drop_items:
            message = render_to_string('email/email_problemtype.html', { "problem_type": drop_items })
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
        if curState != None:
            resolveSection.content = "%s ---> %s" % (curState, state)
        else:
            resolveSection.content = curState
        self.appendSection(resolveSection)

    def addCommentSection(self, user, comment):
        """
        """
        self.appendSection(EmailSection(
            "Comment from %s" % (user.username), comment))
