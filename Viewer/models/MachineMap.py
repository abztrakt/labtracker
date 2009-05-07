import os

from django.db import models 
from django.conf import settings

from labtracker.Viewer.models import base
import labtracker.Viewer.utils 
import labtracker.LabtrackerCore.models as c_models
import labtracker.Machine.models as m_models

app_name = __name__.split('.')[-3]

class MachineMap(base.ViewCore):
    view = models.OneToOneField(base.ViewCore, parent_link=True, editable=False)
    #groups = models.ManyToManyField(m_models.Group, related_name="view_machinemap_groups")
    
    def save(self):
        newmap = self.type_id == None
        self.type = labtracker.Viewer.utils.getViewType(__name__)
        super(MachineMap,self).save()

        if newmap:
            """
            Need to create directories for images
            """
            # create directory need to save image to
            css_dir = '%s/static/css/%s/%s/%s' % \
                (settings.APP_DIR, app_name, self.type.name, self.name)

            if not os.path.isdir(css_dir):
                os.mkdir(css_dir)
            
    def delete(self):
        self.view.delete()
        super(MachineMap,self).delete()   # delete self

    @models.permalink
    def get_absolute_url(self):
        return ('Viewer-MachineMap-view', [str(self.shortname)])

    @models.permalink
    def get_absolute_edit_url(self):
        return ('Viewer-MachineMap-edit', [str(self.shortname)])

    def getUnmappedItems(self):
        """
        Returns a list of items that have not been mapped yet
        """
        mapped = self.getMappedItems()
        mapped_set = set([m_item.machine for m_item in mapped])

        #groups = self.groups.all()
        unmapped = []

        for group in c_models.Group.objects.all(): #groups:
            items = group.items.all()
            unmapped.extend( set(items).difference(mapped_set) )

        return unmapped


    def getMappedItems(self):
        """
        Returns a list of the Items that are currently in use by the view
        """
        return MachineMap_Item.objects.filter(view=self)

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
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s -- %s (%d, %d)" % \
            (self.view, self.machine, self.xpos, self.ypos)

    class Meta:
        app_label = "Viewer"

        unique_together = (
            ('machine', 'view')
        )

