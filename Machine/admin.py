from datetime import datetime

from django.contrib import admin
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms

from Machine import models as mmod


class ContactInLine(admin.TabularInline):
    model = mmod.Contact
    max_num = 2


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    fieldsets = (
            (None, {'fields': ('name', 'description')}),
        )


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type','location','ip','mac1','mac2', 'mac3', 
            'date_added','uw_tag', 'verified', 'usable',)
    search_fields = ['name','ip','location__name','mac1', 'mac2', 'mac3', 'wall_port']
    list_filter = ['type','location__name','date_added','verified','unusable',]
    prepopulated_fields = {"slug": ("name",)}
    actions = ['set_to_not_retired', 'set_to_retired', 'set_to_unverified', 'set_to_verified', 'set_to_unusable', 'set_to_usable', 
        'append_to_comment', 'change_comment', 'change_dates', 'change_location', 'add_to_groups', 'remove_from_groups']


    class ModifyCommentForm(forms.Form):
        """ The form used by append_to_comment and change_comment admin actions.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        comment_submission = forms.CharField(widget=forms.Textarea, required=False)

    class ModifyDateForm(forms.Form):
        """ The form used by the change_dates admin action.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        set_purchase_date = forms.BooleanField(required=False)
        set_warranty_date = forms.BooleanField(required=False)
        set_stf_date = forms.BooleanField(required=False)
        date_submission = forms.DateField(widget=admin.widgets.AdminDateWidget())

    class ModifyLocationForm(forms.Form):
        """ The form used by the change_location admin action.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        location = forms.ModelChoiceField(mmod.Location.objects)

    class ModifyGroupForm(forms.Form):
        """ The form used by add_to_groups and remove_from_groups admin actions.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        group = forms.ModelMultipleChoiceField(mmod.Group.objects)


    def add_to_groups(self, request, queryset):
        if 'submit' in request.POST:
            form = self.ModifyGroupForm(request.POST)
            if form.is_valid():
                #TODO: is this group a real group obj, or just a name?
                groups = form.cleaned_data['group']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            groups_updated = 0
            items_updated = 0
            for group in groups:
                # TODO: find a better way to handle this than resetting the counter every time
                items_updated = 0
                # TODO: look for a better way to add all the items, like update()?
                for item in queryset:
                    group.items.add(item)
                    items_updated += 1
                groups_updated += 1

            if groups_updated == 1:
                message_bit = "1 group"
            else:
                message_bit = "%s groups" % groups_updated

            if items_updated == 1:
                message_bit = "1 item to %s." % message_bit
            else:
                message_bit = "%s items to %s." % (items_updated, message_bit)
            self.message_user(request, "Added %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            form = self.ModifyGroupForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'add_to_groups'
        return render_to_response('admin/mod_group.html', {'mod_group_form': form, 'selected_action': selected_action}, 
            context_instance=RequestContext(request, {'title': 'Modify Group Membership',}))
    add_to_groups.short_description = "Add selected items to groups"

    #TODO OMG, do I really have to duplicate this just to change adds to removes? Kill the redundancy!
    def remove_from_groups(self, request, queryset):
        if 'submit' in request.POST:
            form = self.ModifyGroupForm(request.POST)
            if form.is_valid():
                #TODO: is this group a real group obj, or just a name?
                groups = form.cleaned_data['group']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            groups_updated = 0
            items_updated = 0
            for group in groups:
                # TODO: find a better way to handle this than resetting the counter every time
                items_updated = 0
                # TODO: look for a better way to add all the items, like update()?
                for item in queryset:
                    group.items.remove(item)
                    items_updated += 1
                groups_updated += 1

            if groups_updated == 1:
                message_bit = "1 group"
            else:
                message_bit = "%s groups" % groups_updated

            if items_updated == 1:
                message_bit = "1 item from %s." % message_bit
            else:
                message_bit = "%s items from %s." % (items_updated, message_bit)
            self.message_user(request, "Removed %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            form = self.ModifyGroupForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'remove_from_groups'
        return render_to_response('admin/mod_group.html', {'mod_group_form': form, 'selected_action': selected_action}, 
            context_instance=RequestContext(request, {'title': 'Modify Group Membership',}))
    remove_from_groups.short_description = "Remove selected items from groups"
    
    def change_location(self, request, queryset):
        if 'submit' in request.POST:
            form = self.ModifyLocationForm(request.POST)
            if form.is_valid():
                location = form.cleaned_data['location']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            items_updated = 0
            for i in queryset:
                i.location = location
                i.save()
                items_updated += 1

            if items_updated == 1:
                message_bit = "location for 1 item."
            else:
                message_bit = "location for %s items." % items_updated
            self.message_user(request, "Changed %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            # Set up a blank form BUT with the fact that it's an admin action prepopulated in a hidden field.
            form = self.ModifyLocationForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'change_location'
        return render_to_response('admin/mod_location.html', {'mod_location_form': form, 'selected_action': selected_action}, 
            context_instance=RequestContext(request, {'title': 'Change Location',}))
    change_location.short_description = "Change location for selected items"

    def append_to_comment(self, request, queryset):
        if 'submit' in request.POST:
            form = self.ModifyCommentForm(request.POST)
            if form.is_valid():
                comment_add = form.cleaned_data['comment_submission']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            items_updated = 0
            for i in queryset:
                i.comment += "\n-- comment appended %s --\n%s" % (datetime.now().ctime(), comment_add)
                i.save()
                items_updated += 1

            if items_updated == 1:
                message_bit = "comment to 1 item."
            else:
                message_bit = "comments to %s items." % items_updated
            self.message_user(request, "Appended %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            # Set up a blank form BUT with the fact that it's an admin action prepopulated in a hidden field.
            form = self.ModifyCommentForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'append_to_comment'
        return render_to_response('admin/mod_comment.html', {'mod_comment_form': form, 'selected_action': selected_action}, 
            context_instance=RequestContext(request, {'title': 'Append to Comment',}))
    append_to_comment.short_description = "Append a comment to selected items"

    def change_comment(self, request, queryset):
        if 'submit' in request.POST:
            form = self.ModifyCommentForm(request.POST)
            if form.is_valid():
                comment_change = form.cleaned_data['comment_submission']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            items_updated = 0
            for i in queryset:
                i.comment = comment_change
                i.save()
                items_updated += 1

            if items_updated == 1:
                message_bit = "comment for 1 item."
            else:
                message_bit = "comments for %s items." % items_updated
            self.message_user(request, "Changed %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            # Set up a blank form BUT with the fact that it's an admin action prepopulated in a hidden field.
            form = self.ModifyCommentForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'change_comment'
        return render_to_response('admin/mod_comment.html', {'mod_comment_form': form, 'selected_action': selected_action},
            context_instance=RequestContext(request, {'title': 'Modify Comment',}))
    change_comment.short_description = "Set a comment on selected items"

    def change_dates(self, request, queryset):
        if 'set' in request.POST:
            form = self.ModifyDateForm(request.POST)
            if form.is_valid():
                types = []
                if form.cleaned_data['set_purchase_date'] == True:
                    types.append('purchase_date')
                if form.cleaned_data['set_warranty_date'] == True:
                    types.append('warranty_date')
                if form.cleaned_data['set_stf_date'] == True:
                    types.append('stf_date')
                date_change = form.cleaned_data['date_submission']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            items_updated = 0
            for i in queryset:
                for type in types:
                    setattr(i, type, date_change)
                i.save()
                items_updated += 1

            if items_updated == 1:
                message_bit = "date for 1 item."
            else:
                message_bit = "dates for %s items." % items_updated
            self.message_user(request, "Changed %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            # Set up a blank form BUT with the fact that it's an admin action prepopulated in a hidden field.
            form = self.ModifyDateForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'change_dates'
        return render_to_response('admin/mod_date.html', {'mod_date_form': form,
            'selected_action': selected_action},
            context_instance=RequestContext(request, {'title': 'Modify Date',}))
    change_dates.short_description = "Set dates for selected items"

    def set_to_not_retired(self, request, queryset):
        items_updated = queryset.update(retired=False)
        if items_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % items_updated
        self.message_user(request, "%s successfully marked as not retired." % message_bit)
    set_to_not_retired.short_description = "Mark selected as not retired"

    def set_to_retired(self, request, queryset):
        items_updated = queryset.update(retired=True)
        if items_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % items_updated
        self.message_user(request, "%s successfully marked as retired." % message_bit)
    set_to_retired.short_description = "Mark selected as retired"

    def set_to_unverified(self, request, queryset):
        items_updated = queryset.update(verified=False)
        if items_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % items_updated
        self.message_user(request, "%s successfully marked as unverified." % message_bit)
    set_to_unverified.short_description = "Mark selected as unverified"

    def set_to_verified(self, request, queryset):
        items_updated = queryset.update(verified=True)
        if items_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % items_updated
        self.message_user(request, "%s successfully marked as verified." % message_bit)
    set_to_verified.short_description = "Mark selected as verified"

    def set_to_unusable(self, request, queryset):
        items_updated = queryset.update(unusable=True)
        if items_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % items_updated
        self.message_user(request, "%s successfully marked as unusable." % message_bit)
    set_to_unusable.short_description = "Mark selected as unusable"

    def set_to_usable(self, request, queryset):
        items_updated = queryset.update(unusable=False)
        if items_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % items_updated
        self.message_user(request, "%s successfully marked as usable." % message_bit)
    set_to_usable.short_description = "Mark selected as usable"

class GroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'is_lab', 'casting_server', 'gateway',
            'items', 'description')}),
    )
    list_display = ('name','is_lab','casting_server','gateway')
    inlines = [
        ContactInLine,
    ]
    filter_horizontal = ('items',)


admin.site.register(mmod.Item, ItemAdmin)
admin.site.register(mmod.Group, GroupAdmin)
admin.site.register(mmod.Platform)
admin.site.register(mmod.Type)
admin.site.register(mmod.Location)
admin.site.register(mmod.Status)

# history here for development, remove for production
admin.site.register(mmod.History)

