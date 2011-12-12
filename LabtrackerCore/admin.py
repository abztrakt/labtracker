from django.contrib import admin
from django.db import models

from LabtrackerCore import models as cmod

class GroupAdmin(admin.ModelAdmin):
   filter_horizontal = ('items',) 
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(cmod.Item, ItemAdmin)
admin.site.register(cmod.Group, GroupAdmin)
