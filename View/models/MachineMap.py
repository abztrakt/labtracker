from django.db import models 

from labtracker.View.models import base
import labtracker.View.utils 
import labtracker.LabtrackerCore.models as c_models

class MachineMap(base.ViewCore):
    view = models.OneToOneField(base.ViewCore, parent_link=True, editable=False)

    def delete(self):
        self.view.delete()
        super(MachineMap,self).delete()   # delete self

    def save(self):
        self.type = labtracker.View.utils.getViewType(__name__)
        super(MachineMap,self).save()

    class Admin:
        pass

    class Meta:
        app_label = "View"

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
        app_label = "View"

class MachineMap_Item(models.Model):
    """
    This table is used by the machine map view to determine where computers are
    located
    """
    ORIENTATION_CHOICES = (
        ('H', 'Horizontal'),
        ('V', 'Vertical'),
    )

    view = models.ForeignKey(MachineMap)
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

    class Meta:
        app_label = "View"

