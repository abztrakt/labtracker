from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save

from IssueTracker import utils
from IssueTracker import changedIssueSignal, forms, Email
from IssueTracker.models import Issue, IssueComment, ResolveState

def sendCreateIssueEmail(sender, instance=None, created=False, **kwargs):
    """
    Send an email for issue creation to the reporter, group contact, and CC
    """
    # retrieve the group from Instance
    if instance.group == None and instance.item == None or not created:
        return

    contacts = [c.email for c in utils.getIssueContacts(instance)]

    # send an email to this contact
    em = Email.NewIssueEmail(instance, "New issue Reported")
    try:
        em.addTo(instance.reporter.email)
    except:
        pass
    em.addProblemTypeSection("", instance.problem_type.all())
    em.addCommentSection(None, "Submitted by " + instance.reporter.username + ".\n"
             + instance.description)

    for email in contacts:
        try:
            em.addTo(email)
        except:
            pass
    em.send()

post_save.connect(sendCreateIssueEmail, sender=Issue)

def stateChangeNotifications(sender, data=None, **kwargs):
    """
    Sends notification e-mails on state changes for an issue
    """
    if sender.group == None and sender.item == None:
        return
    #print data
    sender = Issue.objects.get(pk=sender.pk)
    if data['assignee'] != '':
        new_assignee = User.objects.get(pk=data['assignee'])
    contacts = [c.email for c in utils.getIssueContacts(sender)]
    if data['assignee'] != '' and new_assignee.email not in contacts:
        contacts.append(new_assignee.email)

    # send an email to this contact
    em = Email.NewIssueEmail(sender)
    try:
        em.addTo(sender.reporter.email)
    except:
        pass
    # Check for a change in assignee
    if new_assignee != sender.assignee:
        em.addAssigneeSection(str(sender.assignee),str(new_assignee))
    # Check for a change in resolved state
    if data['resolved_state'] != '':
        resolved_state = ResolveState.objects.get(pk=data['resolved_state']) 
        if resolved_state != sender.resolved_state:
            em.addResolveStateSection(resolved_state)
    #Add Comment if exists
    if data['comment'] != '':
        em.addCommentSection(User.objects.get(pk=data['user']), data['comment'])
    for email in contacts:
        try:
            em.addTo(email)
        except:
            pass
    em.send()

changedIssueSignal.connect(stateChangeNotifications)

