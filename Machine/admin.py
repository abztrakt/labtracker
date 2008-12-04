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
            'wall_port','date_added','manu_tag','uw_tag')
    search_fields = ['name','ip','mac','wall_port']
    list_filter = ['type','date_added']

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

