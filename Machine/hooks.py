from django.template import RequestContext
from django.template.loader import render_to_string
from IssueTracker.utils import issueHook

import models, forms

@issueHook("create")
def issueCreate(request):
    """
    Given request, render what extra stuff is needed for Machines
    """
    args = {
        'statusForm' : forms.itemStatusForm(),
    }
    return render_to_string('issueCreate.html', args,
            context_instance=RequestContext(request))

@issueHook("createSubmit")
def issueCreateSave(request, item=None, group=None):
    """
    Hook for handling saving of issue creation, returns True/False
    """

    if item == None and group == None:
        return True

    data = request.POST.copy()

    # update the statuses for the issue
    # instance passed is an issue, so we need to get the Machine out of it
    form = forms.itemStatusForm(data)

    if form.is_valid():
        return form.save(machine=item, group=group)

    return False

@issueHook("view")
def issueView(context, issue):
    """
    Hook for handling the viewing of an issue, should return machine specific
    info
    """

    args = {
        'item': None,
        'group': None
    }
    
    if issue.item != None:
        item = issue.item.item
        args['item'] = item
        args['status'] = item.status.all()
    if issue.group != None:
        args['group'] = issue.group.group

    return render_to_string('issueView.html', args, context)

@issueHook("update")
def issueUpdateView(context, issue):
    """
    Hook for showing form needed for issueUpdateView
    """
    
    args = {
        "form": forms.UpdateMachineForm(),
    }

    return render_to_string('issueUpdate.html', args, context)
