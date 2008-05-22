import unittest

from django.db import models
from django.contrib.auth.models import User

import LabtrackerCore.utils as utils
import LabtrackerCore.models as core

class Status(models.Model):
    """
    Status of the machine
    """

    ms_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    inuse = models.BooleanField(default=False)
    usable = models.BooleanField(default=True)
    broken = models.BooleanField(default=False)
    description = models.CharField(max_length=400, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural="Status"

    class Admin:
        list_display = ('name','inuse','usable','broken', 'description')
        fields = (
            (None, {'fields': ('name', ('inuse','usable','broken',), 'description')}),
        )

class Platform(models.Model):
    """
    Machine Platform: windows XP, Vista, Mac OS X, Linux/Ubuntu, etc.
    """

    platform_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=400, blank=True)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

class Type(models.Model):
    """
    Type of Machine, not InventoryType, similar to a group
    """

    mt_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    platform = models.ForeignKey(Platform)
    model_name = models.CharField(max_length=60)
    specs = models.TextField()
    purchase_date = models.DateField(null=True)
    warranty_date = models.DateField(null=True)
    description = models.CharField(max_length=400, blank=True)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

class Location(models.Model):
    ml_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    building = models.CharField(max_length=60, null=True)
    floor = models.SmallIntegerField(null=True)
    room = models.CharField(max_length=30, null=True)
    comment = models.CharField(max_length=600)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

class Item(core.Item):
    """
    The Machine
    """
    core = models.OneToOneField(core.Item, parent_link=True, editable=False)
    mt = models.ForeignKey(Type, verbose_name='Machine Type')
    ms = models.ForeignKey(Status, verbose_name='Machine Status')
    ml = models.ForeignKey(Location, verbose_name='Location')
    ip = models.IPAddressField(verbose_name="IP Address")
    mac = models.CharField(max_length=17, verbose_name='MAC Address')
    date_added = models.DateTimeField(auto_now_add=True)

    manu_tag = models.CharField(max_length=200, verbose_name="Manufacturers tag")
    comment = models.CharField(max_length=400, blank=True)

    def __unicode__(self):
        return self.item.name

    def delete(self):
        self.item.delete()          # delete the item in core.Item
        super(Item,self).delete()   # delete self

    def save(self):
        self.it = utils.getInventoryType(__name__)
        super(Item,self).save()

    class Admin:
        list_display = ('name', 'mt','ms','ml','ip','mac','date_added','manu_tag')
        search_fields = ['name','ip','mac']
        list_filter = ['mt','ms','date_added']

class Group(core.Group):
    """
    Expands on the core.Group 
    """
    core = models.OneToOneField(core.Group, parent_link=True, editable=False)
    is_lab = models.BooleanField(core=True)
    casting_server = models.IPAddressField()
    gateway = models.IPAddressField()

    def __unicode__(self):
        return self.group.name

    def delete(self):
        self.group.delete()
        super(Group,self).delete()

    def save(self):
        self.it = utils.getInventoryType(__name__)
        super(Group,self).save()

    class Admin:
        fields = (
            (None, {'fields': ('name', 'is_lab', 'casting_server', 'gateway',
                'item', 'description')}),
        )
        list_display = ('name','is_lab','casting_server','gateway')

class History(models.Model):
    mh_id = models.AutoField(primary_key=True)
    machine = models.ForeignKey(Item)
    ms = models.ForeignKey(Status)
    user = models.ForeignKey(core.LabUser)
    time = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    mg = models.ForeignKey(Group, edit_inline=models.TABULAR,num_in_admin=2)

    user = models.ForeignKey(User,core=True)
    is_primary = models.BooleanField(core=True,default=False)

    def __unicode__(self):
        extra = ("", " (Primary)")[self.is_primary]
        return "%s - %s%s" % (self.mg, self.user, extra)

"""
Test Cases
"""
class MachineItemTest(unittest.TestCase):
    def setUp(self):
        """
        A create a machine item
        """
        self.name = "test_name_a"
        print Type.objects.all()
        self.item = Item.objects.create(name=self.name, 
                mt=Type.objects.all()[0], 
                mt=Status.objects.all()[0], 
                ml=Location.objects.all()[0], 
                ip="138.121.342.11", 
                mac="00:34:A3:DF:XA:89",
                manu_tag="manufactuer tag", 
                comment="comment")

    def testParent(self):
        """
        Test and see if the parent exists
        """
        parent = core.Item.objects.get(name=self.name)
        assertEquals(parent.item.name, self.name)
