"""
These are the Core models for Labtracker

"""
import unittest
from hashlib import md5
from django.db import models,connection
#from django.core.exceptions import ImproperlyConfigured
#import django.core.management as dman
import django.db.models.loading as dbload

class LabUser(models.Model):
    """
    Not associated with the actually authenticated users, this only keeps track
    of users logging in/out of the computers. For a list of users for the auth
    list, please look at the django.contrib.auth.models
    """
    user_id = models.CharField(primary_key=True, max_length=32)
    accesses = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user_id

class InventoryType(models.Model):
    """
    This holds all the Inventory Types. 
    E.g.: computer vs. scanner vs. projector
    """

    inv_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    namespace = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=2616)

    def getApp(self):
        """
        return the application
        """
        return __import__(self.namespace)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    """
    Actual items, could be of any inventorytype
    """

    item_id = models.AutoField(primary_key=True)
    it = models.ForeignKey(InventoryType, editable=False)
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    def unresolved_issues(self):
        """
        return all unresolved issues for an item
        """
        return self.issue_set.filter(resolved_state__isnull=True)

    def __unicode__(self):
        """
        Will take the actual item name from whatever the Namespace_namespace
        """
        return self.name

class Group(models.Model):
    """
    Groups the items, can either by group of one inventorytype or all inventorytypes
    """

    group_id = models.AutoField(primary_key=True)
    it = models.ForeignKey(InventoryType, null=True, blank=True)
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=2616)

    items = models.ManyToManyField(Item, null=True, blank=True)

    def __unicode__(self):
        """
        Print out the name of the group
        """
        return self.name

"""
Tests begin here. For the core items, there isn't much to test though
"""

class LabUserTest(unittest.TestCase):
    def setUp(self):
        self.bob_md5 = md5('bob').hexdigest()
        self.bob = LabUser.objects.create(user_id=self.bob_md5)

    def testBasic(self):
        """
        Test basic creation of the user
        """
        self.assertEquals(self.bob.user_id, self.bob_md5)

class InventoryTypeTest(unittest.TestCase):
    def setUp(self):
        pass

