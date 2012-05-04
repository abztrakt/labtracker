from django.contrib import admin
from django.db import models

from Viewer import models as vmod

admin.site.register(vmod.ViewType)

class MachineMapAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups',)

class MachineMap_ItemAdmin(admin.ModelAdmin):
    list_display = ('machine', 'view','size','xpos','ypos','orientation', 
            'date_added', 'last_modified')
    search_fields = ['machine__name', 'view__name', 'size__name', 'orientation', 'ypos', 'xpos',]
    list_filter = ['view', 'size', 'orientation', 'date_added',]
    fieldsets = (
        (None, {'fields': ('machine', 'view', 'size', 'xpos',
            'ypos', 'orientation')}),
    )
class MachineMap_SizeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(vmod.MachineMap)
admin.site.register(vmod.MachineMap_Size, MachineMap_SizeAdmin)
admin.site.register(vmod.MachineMap_Item, MachineMap_ItemAdmin)

