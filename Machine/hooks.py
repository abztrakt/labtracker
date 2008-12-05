from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from IssueTracker.utils import issueHook
import models, forms

@issueHook("create")
def issueCreate(request):
    args = {
        'statusForm' : forms.itemStatusForm(),
    }
    return render_to_response('issueCreate.html', args,
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

