from django.contrib.auth.models import User

from IssueTracker import utils
from IssueTracker import models as im, newIssueSignal, forms, Email

def sendCreateIssueEmail(sender, instance=None, **kwargs):
    """
    Send an email for issue creation to the group contact
    """
    # retrieve the group from Instance
    if instance.group == None and instance.item == None:
        return

    contacts = [c.email for c in utils.getIssueContacts(instance)]

    if len(contacts) == 0:
        return
    
    # send an email to this contact
    em = Email.NewIssueEmail(instance)
    for email in contacts:
        em.addTo(email)
    em.send()

newIssueSignal.connect(sendCreateIssueEmail)
