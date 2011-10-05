from django.contrib import admin
from django.db import models

from LabtrackerCore import models as cmod

class GroupAdmin(admin.ModelAdmin):
   filter_horizontal = ('items',) 


admin.site.register(cmod.Group, GroupAdmin)
