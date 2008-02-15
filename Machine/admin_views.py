from django import newforms as forms, template
from django.newforms import ModelForm
from django.newforms.forms import BaseForm      #, SortedDictFromList
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import django.http as http

from IssueTracker.models import *
import Machine.models as machineModels
import LabtrackerCore.models as coreModels
import LabtrackerCore.forms as coreForms

register = template.Library()

def item(request, core_form, model_form, change=False, add=False):

    model = machineModels.Item
    opts = model._meta

    context = template.RequestContext(request, {
        "opts"                  : opts,
        "add"                   : add,
        "change"                : change,
        "is_popup"              : "_popup" in request.REQUEST
    })

    context.update({
        'has_delete_permission' : context['perms']['Machine'][opts.get_delete_permission()],
        'has_change_permission' : context['perms']['Machine'][opts.get_change_permission()],
        "show_delete"           : not context['add']
    })

    context.update(submit_row(context))

    return render_to_response(
        "admin/Machine/item/change_form.html",
        {
            'addForm'           : model_form,
            'coreForm'          : core_form,
        },
        context
    )

@staff_member_required
def modItem(request, id):
    machineItem = get_object_or_404(machineModels.Item, pk=id)
    coreItem = machineItem.item

    if request.method == "POST":
        model_form = MachineForm(request.POST, instance=machineItem)
        core_form = coreForms.BaseItemForm(request.POST, instance=coreItem)

        if core_form.is_valid() and model_form.is_valid():
            model_form.save()
            core_form.save()

            # TODO redirect like the admin page does 
            return http.HttpResponseRedirect('/admin/Machine/item/')
        else:
            print "Error happened while trying to validate"
    else:
        core_form = coreForms.BaseItemForm(instance=coreItem)
        model_form = MachineForm(instance=machineItem)

    return item(request, core_form, model_form, change=True)




@staff_member_required
def addItem(request):

    if request.method == "POST":
        data = request.POST.copy()

        add_form = MachineForm(data)
        base_form = coreForms.BaseItemForm(data)


        if base_form.is_valid() and add_form.is_valid():
            new_machine = add_form.save(commit=False)
            new_machine.save(data['name'])

            # TODO redirect like the admin page does 
            return http.HttpResponseRedirect('/admin/Machine/item/')
        else:
            print "Error happened while trying to validate"

    else:
        model_form = MachineForm()
        core_form = coreForms.BaseItemForm()

    return item(request, core_form, model_form, add=True)


# helper methods

def submit_row(context):
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    return {
        'onclick_attrib': (opts.get_ordered_objects() and change
                            and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and (change or context['show_delete'])),
        'show_save_as_new': not is_popup and change and opts.admin.save_as,
        'show_save_and_add_another': not is_popup and (not opts.admin.save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'show_save': True
    }

class MachineForm(ModelForm):
    class Meta:
        model = machineModels.Item
        fields=('id', 'item_id', 'mt', 'ms', 'ml', 'ip', 'mac', 'date_added', 'manu_tag', 'comment')

