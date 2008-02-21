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

###################################
#  Methods to modify/add Items    #

@staff_member_required
def modItem(request, id):
    """
    Modify a pre-existing Machine.Item
    Takes request and the id 
    """
    machine_item = get_object_or_404(machineModels.Item, pk=id)
    core_item = machineItem.item

    if request.method == "POST":
        # If the user has submitted stuff, form with stuff filled in
        model_form = MachineForm(request.POST, instance=machineItem)
        core_form = coreForms.BaseItemForm(request.POST, instance=core_item)

        if core_form.is_valid() and model_form.is_valid():
            model_form.save()
            core_form.save()

            # TODO implement redirection depending on which button pressed
            return http.HttpResponseRedirect('/admin/Machine/item/')
        else: 
            # TODO do tricky error handling stuff like the global error message
            # that admin page has by default
            pass

    else:
        core_form = coreForms.BaseItemForm(instance=core_item)
        model_form = MachineForm(instance=machine_item)

    return adminRender(request, machineModels.Item, core_form, model_form, change=True)


@staff_member_required
def addItem(request):
    """
    Add a new Machine.Item, takes nothing but the request object
    """
    if request.method == "POST":
        data = request.POST.copy()

        model_form = MachineForm(data)
        core_form = coreForms.BaseItemForm(data)

        if core_form.is_valid() and model_form.is_valid():
            new_machine = model_form.save(commit=False)
            new_machine.save(data['name'])

            # TODO implement redirection depending on which button pressed
            return http.HttpResponseRedirect('/admin/Machine/item/')
        else:
            # TODO do tricky error handling stuff like the global error message
            # that admin page has by default
            pass

    else:
        model_form = MachineForm()
        core_form = coreForms.BaseItemForm()

    return adminRender(request, machineModels.Item, core_form, model_form, add=True)


###################################

###################################
#  Methods to modify/add Groups   #

@staff_member_required
def modGroup(request, id):
    model = machineModels.Group
    machine_group = get_object_or_404(model, pk=id)
    core_item = machine_group.group

    if request.method == "POST":
        model_form = MachineGroupForm(request.POST, instance=machine_group)
        core_form = coreForms.BaseGroupForm(request.POST, instance=core_item)

        if core_form.is_valid() and model_form.is_valid():
            model_form.save()
            core_form.save()

            # TODO implement redirection depending on which button pressed
            return http.HttpResponseRedirect('/admin/Machine/group/')
        else:
            # TODO do tricky error handling stuff like the global error message
            # that admin page has by default
            pass
    else:
        core_form = coreForms.BaseGroupForm(instance=core_item)
        model_form = MachineGroupForm(instance=machine_group)

    return adminRender(request, model, core_form, model_form, change=True)


@staff_member_required
def addGroup(request):
    model = machineModels.Group

    if request.method == "POST":
        data = request.POST.copy()

        model_form = MachineGroupForm(data)
        core_form = coreForms.BaseGroupForm(data)

        if core_form.is_valid() and model_form.is_valid():
            new_machine_group = model_form.save(commit=False)
            new_machine_group.save(data['name'], data['description'])

            # TODO implement redirection depending on which button pressed
            return http.HttpResponseRedirect('/admin/Machine/group/')
        else:
            # TODO do tricky error handling stuff like the global error message
            # that admin page has by default
            pass
    else:
        model_form = MachineGroupForm()
        core_form = coreForms.BaseGroupForm()

    return adminRender(request, model, core_form, model_form, add=True)

###################################


###################################
#         helper methods

def adminRender(request, model, core_form, model_form, change=False, add=False):
    """
    Utilized as a wrapper to the administration templates, creates the variables
    needed by the form.
    """

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
        "Machine/admin/change_form.html",
        {
            'addForm'           : model_form,
            'coreForm'          : core_form,
        },
        context
    )

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
        fields = ('id', 'item_id', 'mt', 'ms', 'ml', 'ip', 'mac', 'date_added',
                'manu_tag', 'comment')

class MachineGroupForm(ModelForm):
    class Meta:
        model = machineModels.Group
        fields = ('is_lab', 'casting_server', 'gateway')

