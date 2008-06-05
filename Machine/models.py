from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase

import LabtrackerCore.utils as utils
import LabtrackerCore.models as coreModels

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

class Item(coreModels.Item):
    """
    The Machine
    """
    core = models.OneToOneField(coreModels.Item, parent_link=True, editable=False)
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
        self.core.delete()          # delete the item in coreModels.Item
        super(Item,self).delete()   # delete self

    def save(self):
        self.it = utils.getInventoryType(__name__)
        super(Item,self).save()

    class Admin:
        list_display = ('name', 'mt','ms','ml','ip','mac','date_added','manu_tag')
        search_fields = ['name','ip','mac']
        list_filter = ['mt','ms','date_added']

class Group(coreModels.Group):
    """
    Expands on the coreModels.Group 
    """
    core = models.OneToOneField(coreModels.Group, parent_link=True, editable=False)
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
    user = models.ForeignKey(coreModels.LabUser)
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
class PlatformTest(TestCase):
    def setUp(self):
        """
        Create a platform
        """
        self.name = "ArchLinux"
        self.platform = Platform.objects.create(
                    name = "ArchLinux",
                    description = "ArchLinux distribution"
                )

    def testExistance(self):
        platforms = Platform.objects.filter(name="ArchLinux")
        assert(len(platforms) == 1)
        self.assertEquals(platforms[0], self.platform)

    def tearDown(self):
        self.platform.delete()

class TypeTest(TestCase):
    def setUp(self):
        """
        Create a test item
        """
        self.name = "Gaming Station"
        self.type = Type.objects.create(
                name = "Gaming Station",
                warranty_date = "2008-01-07", 
                model_name = "Dell Optiplex 2002", 
                platform = Platform.objects.all()[0],
                purchase_date = "2008-01-07", 
                specs = "stuff", 
                description = ""
            )

    def tearDown(self):
        self.type.delete()

class StatusTest(TestCase):
    def setUp(self):
        self.name = "test"
        self.status = Status.objects.create(
                broken = False,
                usable = False,
                description = "teststatus",
                name = "test",
                inuse = True
            )
        self.status.save()

    def testExistance(self):
        status = Status.objects.filter(name=self.name)
        assert(len(status) == 1)
        self.assertEquals(status[0], self.status)
        
class LocationTest(TestCase):
    def setUp(self):
        self.name = "test"
        self.location = Location.objects.create(
                building = "test",
                comment = "test",
                room = 101,
                name = self.name,
                floor = 1
            )
        self.location.save()

    def testExistance(self):
        location = Location.objects.filter(name=self.name)
        assert(len(location) == 1)
        self.assertEquals(location[0], self.location)

class MachineItemTest(TestCase):
    def setUp(self):
        """
        A create a machine item
        """

        coreModels.InventoryType.objects.create(
                    name="Machine",
                    namespace="Machine",
                    description="Machine inv type"
                )

        self.platform = Platform.objects.create(
                    name = "ArchLinux",
                    description = "ArchLinux distribution"
                )
        self.platform.save()

        self.type = Type.objects.create(
                name = "Gaming Station",
                warranty_date = "2008-01-07", 
                model_name = "Dell Optiplex 2002", 
                platform = Platform.objects.all()[0],
                purchase_date = "2008-01-07", 
                specs = "stuff", 
                description = ""
            )
        self.type.save()

        self.status = Status.objects.create(
                broken = False,
                usable = False,
                description = "teststatus",
                name = "test",
                inuse = True
            )
        self.status.save()
        
        self.location = Location.objects.create(
                building = "test",
                comment = "test",
                room = 101,
                name = "test",
                floor = 1
            )
        self.location.save()

        self.name = "test_name_a"
        self.item = Item.objects.create(name=self.name, 
                mt=self.type,
                ms=self.status,
                ml=self.location,
                ip="138.121.342.11", 
                mac="00:34:A3:DF:XA:89",
                manu_tag="manufactuer tag", 
                comment="comment")

    def testParent(self):
        """
        Test and see if the parent exists
        """
        parent = coreModels.Item.objects.get(name=self.name)
        self.assertEquals(parent.item.name, self.name)
