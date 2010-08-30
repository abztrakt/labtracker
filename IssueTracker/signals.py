from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save

from IssueTracker import utils
from IssueTracker import changedAssigneeSignal, changedIssueSignal, forms, Email
from IssueTracker.models import Issue, IssueComment

previousAssigneeForIssue = ""

def sendCreateIssueEmail(sender, instance=None, created=False, **kwargs):
    """
    Send an email for issue creation to the reporter, group contact, and CC
    """
    # retrieve the group from Instance
    if instance.group == None and instance.item == None or not created:
        return

    contacts = [c.email for c in utils.getIssueContacts(instance)]
    if previousAssigneeForIssue != None and previousAssigneeForIssue != '' and previousAssigneeForIssue.email not in contacts:
        contacts.append(previousAssigneeForIssue.email)

    # send an email to this contact
    em = Email.NewIssueEmail(instance, "New issue Reported")
    em.addTo(instance.reporter.email)
    em.addProblemTypeSection("", instance.problem_type.all())
    em.addCommentSection(None, "Submitted by " + instance.reporter.username + ".\n"
             + instance.description)

    for email in contacts:
        em.addTo(email)
    em.send()

post_save.connect(sendCreateIssueEmail, sender=Issue)

def stateChangeNotifications(sender, old_issue=None, **kwargs):
    """
    Sends notification e-mails on state changes for an issue
    """
    if sender.group == None and sender.item == None:
        return

    contacts = [c.email for c in utils.getIssueContacts(sender)]
    if old_issue.assignee != None and old_issue.assignee.email not in contacts:
        contacts.append(old_issue.assignee.email)

    # send an email to this contact
    em = Email.NewIssueEmail(sender)
    em.addTo(sender.reporter.email)
    #This broke, need to fix -Yusuke
    #em.addProblemTypeSection("", instance.problem_type.all())
    if old_issue.assignee != sender.assignee:
        em.addAssigneeSection(str(old_issue.assignee),str(sender.assignee))
    em.addResolveStateSection(old_issue.resolved_state)
    #em.addCommentSection(sender.reporter, sender.description)

    for email in contacts:
        em.addTo(email)
    em.send()

changedIssueSignal.connect(stateChangeNotifications)

