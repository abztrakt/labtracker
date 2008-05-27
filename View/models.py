from django.db import models
import django.db.models.loading as dbload

import LabtrackerCore.models as c_models
import Machine.models
from MachineMap import *

class ViewType(models.Model):
    """
    Every type of view is registered here, referenced by View
    """
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=2616)

    def getModel(self):
        return dbload.get_model("View", "%s_item" % self.name)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

class View(models.Model):
    """
    Every view available will be registered here
    """
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=2616)
    groups = models.ManyToManyField(c_models.Group,
            filter_interface=models.HORIZONTAL)
    #items = models.ManyToManyField(c_models.Item, editable=False)
    type = models.ForeignKey(ViewType)

    def getMappedItems(self):
        """
        Returns a list of the Items that are currently in use by the view
        """
        model = self.type.getModel()
        return model.objects.filter(view=self)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

class MachineMap_item(models.Model):
    """
    This table is used by the machine map view to determine where computers are
    located
    """
    ORIENTATION_CHOICES = (
        ('H', 'Horizontal'),
        ('V', 'Vertical'),
    )

    view = models.ForeignKey(View)
    item = models.ForeignKey(c_models.Item)
    size = models.ForeignKey(MachineMap_Size)
    xpos = models.IntegerField()
    ypos = models.IntegerField()
    orientation = models.CharField(max_length=1, choices=ORIENTATION_CHOICES,
            default='H')

    def __unicode__(self):
        return "%s -- %s (%d, %d)" % \
            (self.view, self.item, self.xpos, self.ypos)

    class Admin:
        pass

