from django.db import models 

from labtracker.Viewer.models import base
import labtracker.Viewer.utils 
import labtracker.LabtrackerCore.models as c_models
import labtracker.Machine.models as m_models

class MachineMap(base.ViewCore):
    view = models.OneToOneField(base.ViewCore, parent_link=True, editable=False)
    groups = models.ManyToManyField(m_models.Group,
            filter_interface=models.HORIZONTAL,
            related_name="view_machinemap_groups"
            )

    def save(self):
        self.type = labtracker.Viewer.utils.getViewType(__name__)
        super(MachineMap,self).save()

    def delete(self):
        self.view.delete()
        super(MachineMap,self).delete()   # delete self

    def getUnmappedItems(self):
        """
        Returns a list of items that have not been mapped yet
        """
        mapped = self.getMappedItems()
        mapped_set = set([m_item.machine for m_item in mapped])

        groups = self.groups.all()
        unmapped = []

        for group in groups:
            items = group.items.all()
            unmapped.extend( set(items).difference(mapped_set) )

        return unmapped


    def getMappedItems(self):
        """
        Returns a list of the Items that are currently in use by the view
        """
        return MachineMap_Item.objects.filter(view=self)

    class Admin:
        pass

    class Meta:
        app_label = "Viewer"

class MachineMap_Size(models.Model):
    """
    This holds the allowed sizes for machines
    """
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=2616, blank=True)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        app_label = "Viewer"

class MachineMap_Item(models.Model):
    """
    This table is used by the machine map view to determine where computers are
    located
    """
    ORIENTATION_CHOICES = (
        ('H', 'Horizontal'),
        ('V', 'Vertical'),
    )

    machine = models.ForeignKey(m_models.Item)
    view = models.ForeignKey(MachineMap)
    size = models.ForeignKey(MachineMap_Size)
    xpos = models.IntegerField()
    ypos = models.IntegerField()
    orientation = models.CharField(max_length=1, choices=ORIENTATION_CHOICES,
            default='H')

    def __unicode__(self):
        return "%s -- %s (%d, %d)" % \
            (self.view, self.machine, self.xpos, self.ypos)

    class Admin:
        pass

    class Meta:
        app_label = "Viewer"

        unique_together = (
            ('machine', 'view')
        )

