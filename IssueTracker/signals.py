from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.conf import settings

from IssueTracker import utils
from IssueTracker import newIssueSignal, changedIssueSignal, forms, Email
from IssueTracker.models import Issue, IssueComment, ResolveState, ProblemType

def sendCreateIssueEmail(sender, instance=None, created=False, **kwargs):
    """
    Send an email for issue creation to the reporter, group contact, and CC
    """
    # retrieve the group from Instance
    if instance.group == None and instance.item == None or not created:
        return
    contacts = [c.email for c in utils.getIssueContacts(instance)]

    # send an email to this contact
    em = Email.NewIssueEmail(instance, instance.title)
    
    # if (instance.assignee is None)        
    try:
        em.addTo(instance.reporter.email)
    except:
        pass
    p_types = []
    for p_type in instance.problem_type.all():
        p_types.append(p_type.pk)
    em.addProblemTypeSection("", p_types) 
    if (instance.assignee is None):
        if (instance.steps == '' and instance.attempts ==''):
            em.addCommentSection(None, "Submitted by " + instance.reporter.username + ".\n"
            + "Group/Location: " + instance.group.name + ".\n"     
            + "Machine Name: " + instance.item.name + ".\n"
            + "Description: " + "\n" + instance.description + "\n\n")
        elif instance.steps == '':
            em.addCommentSection(None, "Submitted by " + instance.reporter.username + ".\n"
            + "Group/Location: " + instance.group.name + ".\n"     
            + "Machine Name: " + instance.item.name + ".\n"
            + "Description: " + "\n" + instance.description + "\n\n"
            + "Attempts: " + "\n" + instance.attempts + "\n\n")
        elif instance.attempts == '':
            em.addCommentSection(None, "Submitted by " + instance.reporter.username + ".\n"
            + "Group/Location: " + instance.group.name + ".\n"     
            + "Machine Name: " + instance.item.name + ".\n"
            + "Description: " + "\n" + instance.description + "\n\n"
            + "Steps: " + "\n" + instance.steps + "\n\n")
        else:
            em.addCommentSection(None, "Submitted by " + instance.reporter.username + ".\n"
            + "Group/Location: " + instance.group.name + ".\n"     
            + "Machine Name: " + instance.item.name + ".\n"
            + "Description: " + "\n" + instance.description + "\n\n"
            + "Steps: " + "\n" + instance.steps + "\n\n"
            + "Attempts: " + "\n" + instance.attempts + "\n\n")
    else:
        if (instance.steps == '' and instance.attempts ==''):
            em.addCommentSection(None, "Submitted by " + instance.reporter.username + ".\n"
            + "Assigned to: " + instance.assignee.username + ".\n"
            + "Group/Location: " + instance.group.name + ".\n"     
            + "Machine Name: " + instance.item.name + ".\n"
            + "Description: " + "\n" + instance.description + "\n\n")
        elif (instance.steps == ''):
            em.addCommentSection(None, "Submitted by " + instance.reporter.username + ".\n"
            + "Assigned to: " + instance.assignee.username + ".\n"
            + "Group/Location: " + instance.group.name + ".\n"     
            + "Machine Name: " + instance.item.name + ".\n"
            + "Description: " + "\n" + instance.description + "\n\n"
            + "Attempts: " + "\n" + instance.attempts + "\n\n")
        elif (instance.attempts == ''):
            em.addCommentSection(None, "Submitted by " + instance.reporter.username + ".\n"
            + "Assigned to: " + instance.assignee.username + ".\n"
            + "Group/Location: " + instance.group.name + ".\n"     
            + "Machine Name: " + instance.item.name + ".\n"
            + "Description: " + "\n" + instance.description + "\n\n"
            + "Steps: " + "\n" + instance.steps + "\n\n")
        else:
            em.addCommentSection(None, "Submitted by " + instance.reporter.username + ".\n"
            + "Assigned to: " + instance.assignee.username + ".\n"
            + "Group/Location: " + instance.group.name + ".\n"     
            + "Machine Name: " + instance.item.name + ".\n"
            + "Description: " + "\n" + instance.description + "\n\n"
            + "Steps: " + "\n" + instance.steps + "\n\n"
            + "Attempts: " + "\n" + instance.attempts + "\n\n")

    for email in contacts:
        try:
            em.addTo(email)
        except:
            pass
    em.send()

newIssueSignal.connect(sendCreateIssueEmail)

def stateChangeNotifications(sender, data=None, **kwargs):
    """
    Sends notification e-mails on state changes for an issue
    """
    if sender.group == None and sender.item == None:
        return
    #print data
    sender = Issue.objects.get(pk=sender.pk)
    new_assignee = None
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
    if data.has_key('cc'):
        cc_id = data.getlist('cc')
    else:
        cc_id = []
    cc_list = [] 
    for cc in cc_id:
        try:
            cc_list.append(User.objects.get(pk=cc))
        except:
            pass
    em.addCCSection(sender.cc.filter(), cc_list)
    if new_assignee != sender.assignee:
        em.addAssigneeSection(str(sender.assignee),str(new_assignee))
    # Check for a change in resolved state
    em.addProblemTypeSection(sender.problem_type.filter(), data.getlist('problem_type')) 
    if data['resolved_state'] != '':
        resolved_state = ResolveState.objects.get(pk=data['resolved_state']) 
        if resolved_state != sender.resolved_state:
            em.addResolveStateSection(resolved_state)
    #Add Comment if exists
    if data['comment'] != '':
        em.addCommentSection(User.objects.get(pk=data['user']), data['comment'])
    title = sender.title
    try:
        title = title.replace('@', '[at]')
    except:
        pass    
    em.subject = "[" + settings.EMAIL_SUBJECT_PREFIX + "]" + ' Change to Issue: %s' % (title) 
    for email in contacts:
        try:
            em.addTo(email)
        except:
            pass
    em.send()

changedIssueSignal.connect(stateChangeNotifications)

