from django.contrib import admin
from django.db import models

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
    actions = ['set_to_unverified', 'set_to_verified']

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

