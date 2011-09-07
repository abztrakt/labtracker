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
    list_display = ('name', 'type','location','ip','mac1','mac2',
            'date_added','uw_tag', 'verified',)
    search_fields = ['name','ip','location__name','mac1', 'mac2', 'wall_port']
    list_filter = ['type','location__name','date_added','verified',]
    actions = ['set_to_unverified', 'set_to_verified', 'append_to_comment', 'change_comment', 
        'change_purchase_date']

    class ModifyCommentForm(forms.Form):
        """ The form used by append_to_comment and change_comment admin actions.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        comment_submission = forms.CharField(widget=forms.Textarea, required=False)

    class ModifyDateForm(forms.Form):
        """ The form used by the change_purchase_date admin action.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        date_submission = forms.DateField(widget=admin.widgets.AdminDateWidget())

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

    def change_purchase_date(self, request, queryset):
        if 'set' in request.POST:
            form = self.ModifyDateForm(request.POST)
            if form.is_valid():
                date_change = form.cleaned_data['date_submission']
            else:
                for key in form.errors.keys():
                    self.message_user(request, "%s: %s" % (key, form.errors[key].as_text()))
                return HttpResponseRedirect(request.get_full_path())

            items_updated = 0
            for i in queryset:
                i.purchase_date = date_change
                i.save()
                items_updated += 1

            if items_updated == 1:
                message_bit = "purchase date for 1 item."
            else:
                message_bit = "purchase dates for %s items." % items_updated
            self.message_user(request, "Changed %s" % message_bit)

            return HttpResponseRedirect(request.get_full_path())

        else:
            # Set up a blank form BUT with the fact that it's an admin action prepopulated in a hidden field.
            form = self.ModifyDateForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        selected_action = 'change_purchase_date'
        return render_to_response('admin/mod_date.html', {'mod_date_form': form,
            'selected_action': selected_action},
            context_instance=RequestContext(request, {'title': 'Modify Date',}))

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


class GroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'is_lab', 'casting_server', 'gateway',
            'items', 'description')}),
    )
    list_display = ('name','is_lab','casting_server','gateway')
    inlines = [
        ContactInLine,
    ]


admin.site.register(mmod.Item, ItemAdmin)
admin.site.register(mmod.Group, GroupAdmin)
admin.site.register(mmod.Platform)
admin.site.register(mmod.Type)
admin.site.register(mmod.Location)
admin.site.register(mmod.Status)

# history here for development, remove for production
admin.site.register(mmod.History)

