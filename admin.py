from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as AuthGroup 

from labtracker.LabtrackerCore.models import Group as c_Group
from labtracker.IssueTracker.models import ResolveState, ProblemType
from labtracker.Machine.models import Status, Platform, Type, Location, Item, Group
from labtracker.Viewer.models import ViewType
from labtracker.Viewer.models.MachineMap import MachineMap, MachineMap_Size, MachineMap_Item

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name','inuse','usable','broken', 'description')
    fieldsets = (
            (None, {'fields': ('name', ('inuse','usable','broken',), 'description')}),
        )

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type','status','location','ip','mac1','mac2','wall_port','date_added','manu_tag','uw_tag')
    search_fields = ['name','ip','mac','wall_port']
    list_filter = ['type','status','date_added']

class GroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'is_lab', 'casting_server', 'gateway',
            'items', 'description')}),
    )
    list_display = ('name','is_lab','casting_server','gateway')

class MachineMapAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups',)

class MachineMap_ItemAdmin(admin.ModelAdmin):
    list_display = ('machine', 'view','size','xpos','ypos','orientation', 'date_added', 'last_modified')
    fieldsets = (
        (None, {'fields': ('machine', 'view', 'size', 'xpos',
            'ypos', 'orientation')}),
    )

default_admin = admin.AdminSite()

default_admin.register(c_Group)

default_admin.register(Status, StatusAdmin)
default_admin.register(Platform)
default_admin.register(Type)
default_admin.register(Location)
default_admin.register(Item, ItemAdmin)
default_admin.register(Group, GroupAdmin)

default_admin.register(ResolveState)
default_admin.register(ProblemType)

default_admin.register(ViewType)

default_admin.register(MachineMap)
default_admin.register(MachineMap_Size)
default_admin.register(MachineMap_Item, MachineMap_ItemAdmin)

default_admin.register(User, UserAdmin)
default_admin.register(AuthGroup)
