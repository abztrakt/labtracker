from django.contrib.auth.models import User

from IssueTracker import models as im, newIssueSignal, forms, Email

def sendCreateIssueEmail(sender, instance=None, **kwargs):
    """
    Send an email for issue creation to the group contact
    """
    # retrieve the group from Instance
    if instance.group == None and instance.item == None:
        print "No group or item for instance"
        return

    contacts = []

    if instance.group:
        group = instance.group.group
        g_contacts = group.contact_set.filter(is_primary=True).all()
        contacts = [contact.user.email for contact in g_contacts]

    contacts = set(contacts)

    # now add contacts for item groups 
    i_groups = instance.item.group_set.all()

    # for each group, need to get the contacts
    for g in i_groups:
        ig_contacts = g.group.contact_set.filter(is_primary=True).all()
        contacts = contacts.union([contact.user.email for contact in ig_contacts])

    if len(contacts) == 0:
        return
    
    # send an email to this contact
    em = Email.NewIssueEmail(instance)
    for email in contacts:
        em.addTo(email)
    em.send()

newIssueSignal.connect(sendCreateIssueEmail)
