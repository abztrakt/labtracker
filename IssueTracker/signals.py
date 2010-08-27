from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save

from IssueTracker import utils
from IssueTracker import changedAssigneeSignal, forms, Email
from IssueTracker.models import Issue

previousAssigneeForIssue = ""

def sendCreateIssueEmail(sender, instance=None, **kwargs):
    """
    Send an email for issue creation to the reporter, group contact, and CC
    """
    global previousAssigneeForIssue
    # retrieve the group from Instance
    if instance.group == None and instance.item == None:
        return

    contacts = [c.email for c in utils.getIssueContacts(instance)]
    if previousAssigneeForIssue != None and previousAssigneeForIssue != '' and previousAssigneeForIssue.email not in contacts:
        contacts.append(previousAssigneeForIssue.email)

    # send an email to this contact
    em = Email.NewIssueEmail(instance, "[Issue %d NEW]" % instance.pk)
    em.addTo(instance.reporter.email)
    #This broke, need to fix -Yusuke
    #em.addProblemTypeSection("", instance.problem_type.all())
    em.addCommentSection(instance.reporter, instance.description)

    for email in contacts:
        em.addTo(email)
    em.send()

post_save.connect(sendCreateIssueEmail, sender=Issue)

def preSaveIssueEmail(sender, old_assignee=None, **kwargs):
    """
    We might not even need this, but I'll leave it here for a little bit...
    """
    global previousAssigneeForIssue
    previousAssigneeForIssue = old_assignee

changedAssigneeSignal.connect(preSaveIssueEmail)
