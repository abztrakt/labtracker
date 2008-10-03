from django.contrib import admin
from django.db import models

from Viewer import models as vmod

admin.site.register(vmod.ViewType)

class MachineMapAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups',)

class MachineMap_ItemAdmin(admin.ModelAdmin):
    list_display = ('machine', 'view','size','xpos','ypos','orientation', 
            'date_added', 'last_modified')
    fieldsets = (
        (None, {'fields': ('machine', 'view', 'size', 'xpos',
            'ypos', 'orientation')}),
    )


admin.site.register(vmod.MachineMap)
admin.site.register(vmod.MachineMap_Size)
admin.site.register(vmod.MachineMap_Item, MachineMap_ItemAdmin)

