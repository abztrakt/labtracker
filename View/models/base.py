from django.db import models
import django.db.models.loading as dbload

import LabtrackerCore.models as c_models
import Machine.models

class ViewType(models.Model):
    """
    Every type of view is registered here, referenced by View
    """
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=2616)

    def __save__(self):
        # FIXME need to create the class
        super(ViewType, self).save()

    def getModel(self):
        return dbload.get_model("View", self.name)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        app_label = "View"

class ViewCore(models.Model):
    """
    Every view available will be registered here
    """
    name = models.CharField(max_length=60, unique=True)
    shortname = models.SlugField(max_length=20, unique=True,
            help_text="Used to access view")
    description = models.CharField(max_length=2616)
    groups = models.ManyToManyField(c_models.Group,
            filter_interface=models.HORIZONTAL)
    type = models.ForeignKey(ViewType, editable=False)

    def getMappedItems(self):
        """
        Returns a list of the Items that are currently in use by the view
        """
        model = self.type.getModel()
        return model.objects.filter(view=self)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "View"

