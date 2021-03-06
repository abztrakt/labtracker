import re

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

import LabtrackerCore.utils as utils
import LabtrackerCore.models as coreModels

from datetime import date, datetime

from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["Machine.models.MacField"])
class MacField(models.CharField):
    
    description = "A field for mac addresses"
    default_error_messages = { 
        'invalid': (u'Enter a valid MAC address.'),
    }   

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 17
        kwargs['help_text'] = 'Please use the following format: 00:AA:1B:00:00:00.'
        super(MacField, self).__init__(*args, **kwargs)
    
    def db_type(self, connection):
        return 'char(17)'

    def validate(self, value, model_instance):
        if re.search('^([0-9a-fA-F]{2}([:]?|$)){6}$', value) == None:
            raise ValidationError('Enter a valid MAC address.')
   
class Status(models.Model):
    """
    Status of the machine
    """

    ms_id = models.AutoField(primary_key=True)
    name = models.SlugField(max_length=60, unique=True)
    description = models.CharField(max_length=400, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural="Status"
        unique_together = (("ms_id", "name"),)

class Platform(models.Model):
    """
    Machine Platform: windows XP, Vista, Mac OS X, Linux/Ubuntu, etc.
    """

    platform_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=400, blank=True)

    def __unicode__(self):
        return self.name

class Type(models.Model):
    """
    Type of Machine, not InventoryType, similar to a group
    """

    mt_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    platform = models.ForeignKey(Platform)
    model_name = models.CharField(max_length=60)
    specs = models.TextField()
    description = models.CharField(max_length=400, blank=True)

    def __unicode__(self):
        return self.name

class Location(models.Model):
    ml_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    building = models.CharField(max_length=60, null=True)
    floor = models.SmallIntegerField(null=True, blank=True)
    room = models.CharField(max_length=30, null=True)
    comment = models.CharField(max_length=600)
    usable_threshold = models.IntegerField(default=95)

    def __unicode__(self):
        return self.name

class Item(coreModels.Item):
    """
    The Machine
    """
    core = models.OneToOneField(coreModels.Item, parent_link=True, 
            editable=False)
    type = models.ForeignKey(Type, verbose_name='Machine Type')
    verified = models.BooleanField()
    unusable = models.BooleanField()
    retired = models.BooleanField()
    status = models.ManyToManyField(Status, related_name="machine_status", blank=True)
    
    location = models.ForeignKey(Location, verbose_name='Location')
    ip = models.IPAddressField(verbose_name="IP Address")
    mac1 = MacField(verbose_name='MAC Address') 
    mac2 = MacField(verbose_name='Additional MAC Address', blank=True)
    mac3 = MacField(verbose_name='Additional MAC Address', blank=True)
    wall_port = models.CharField(max_length=25)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    manu_tag = models.CharField(max_length=200, 
            verbose_name="Manufacturers tag")
    uw_tag = models.CharField(max_length=200, verbose_name="UW tag", 
            blank=True, null=True)

    purchase_date = models.DateField(null=True, blank=True)
    warranty_date = models.DateField(null=True, blank=True)
    stf_date = models.DateField(null=True, blank=True, 
            verbose_name='Student Tech Fee Contract Expiration')

    comment = models.TextField(blank=True, null=True)

    def usable(self):
        return (not self.unusable)
    usable.boolean = True

    @models.permalink
    def get_absolute_url(self):
        return ('Machine-detail', [str(self.pk),])

    def primaryContact(self):
        """
        Returns the primary contact for this item, or None if no primary 
        contact exists
        """
        # first check to see if item has groups, then fetch the groups, and 
        # call the groups primary contact function
        return Contact.objects.filter(is_primary=True, mg__items__pk=self.pk)

    def __unicode__(self):
        return self.item.name

    def delete(self):
        self.core.delete()          # delete the item in coreModels.Item
        super(Item,self).delete()   # delete self
    
    def save(self, *args, **kwargs):
        self.it = utils.getInventoryType(__name__)
        super(Item,self).save(*args, **kwargs)

class Group(coreModels.Group):
    """
    Expands on the coreModels.Group 
    """
    core = models.OneToOneField(coreModels.Group, parent_link=True, editable=False)
    is_lab = models.BooleanField()
    casting_server = models.IPAddressField()
    gateway = models.IPAddressField()

    def primaryContact(self):
        """
        for this group find primary contact, returns set of users
        """
        return self.contact_set.filter(is_primary=True)

    def contacts(self):
        """
        Returns the set of all contacts for this group
        """
        return self.contact_set.filter()

    def __unicode__(self):
        return self.group.name

    def delete(self):
        self.group.delete()
        super(Group,self).delete()

    def save(self):
        if (self.it == None):
            self.it = utils.getInventoryType(__name__)
        super(Group,self).save()

class History(models.Model):
    mh_id = models.AutoField(primary_key=True)
    machine = models.ForeignKey(Item)
    ms = models.ManyToManyField(Status, null=True, blank=True)
    user = models.ForeignKey(coreModels.LabUser)
    session_time = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
	return "%s-%s-%s" % (self.machine.location,self.machine.name,self.login_time)

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    mg = models.ForeignKey(Group)

    user = models.ForeignKey(User)
    is_primary = models.BooleanField(default=False)

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
                model_name = "Dell Optiplex 2002", 
                platform = Platform.objects.all()[0],
                specs = "stuff", 
                description = ""
            )

    def tearDown(self):
        self.type.delete()

class StatusTest(TestCase):
    def setUp(self):
        self.name = "test"
        self.status = Status.objects.create(
                description = "teststatus",
                name = "test",
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
                model_name = "Dell Optiplex 2002", 
                platform = Platform.objects.all()[0],
                specs = "stuff", 
                description = ""
            )
        self.type.save()

        self.status = Status.objects.create(
                description = "teststatus",
                name = "test",
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


        self.name = "test_name_abcd"

        self.item = Item.objects.create(
                name=self.name, 
                type=self.type,
                location=self.location,
                purchase_date = "2009-01-07", 
                warranty_date = "2009-01-07", 
                wall_port = "adj",
                ip="18.121.342.11", 
                mac1="00:34:A3:DF:XA:90",
                manu_tag="manufactuer tag", 
                uw_tag="uw tag", 
                comment="comment")
        self.item.status.add(self.status)
        self.item.save()

    def testParent(self):
        """
        Test and see if the parent exists
        """
        parent = coreModels.Item.objects.get(name=self.name)
        self.assertEquals(parent.item.name, self.name)
