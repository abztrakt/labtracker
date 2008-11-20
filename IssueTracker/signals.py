from django.contrib.auth.models import User

from IssueTracker import models as im, newIssueSignal, forms, Email

def sendCreateIssueEmail(sender, instance=None, **kwargs):
    """
    Send an email for issue creation to the group contact
    """
    # retrieve the group from Instance
    if instance.group == None and instance.item == None:
        return

    contacts = []

    if instance.group:
        g_contacts = instance.group.group.primaryContact()
        contacts = [contact.user.email for contact in g_contacts]

    contacts = set(contacts)

    # now add contacts for item groups 
    if instance.item:
        i_contacts = instance.item.item.primaryContact()
        contacts = contacts.union([c.user.email for c in i_contacts])

    if len(contacts) == 0:
        return
    
    # send an email to this contact
    em = Email.NewIssueEmail(instance)
    for email in contacts:
        em.addTo(email)
    em.send()

newIssueSignal.connect(sendCreateIssueEmail)
