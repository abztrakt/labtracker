from django.contrib.auth.models import User

from IssueTracker import utils
from IssueTracker import models as im, newIssueSignal, forms, Email

def sendCreateIssueEmail(sender, instance=None, **kwargs):
    """
    Send an email for issue creation to the reporter, group contact, and CC
    """
    # retrieve the group from Instance
    if instance.group == None and instance.item == None:
        return

    contacts = [c.email for c in utils.getIssueContacts(instance)]

    # send an email to this contact
    em = Email.NewIssueEmail(instance, "[Issue %d NEW]" % instance.pk)
    em.addTo(instance.reporter.email)
    em.addProblemTypeSection("", sender['problem_type'].data)
    em.addCommentSection(instance.reporter, instance.description)

    for email in contacts:
        em.addTo(email)
    em.send()

newIssueSignal.connect(sendCreateIssueEmail)
