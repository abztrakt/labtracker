import os

from django.db import models
from django.conf import settings
import django.db.models.loading as dbload

import LabtrackerCore.models as c_models
import Machine.models

class ViewType(models.Model):
    """
    Every type of view is registered here, referenced by Viewer
    """
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=2616)

    def save(self):
        # FIXME need to create the class
        newtype = self.name == None

        super(ViewType, self).save()

        if newtype:
            app_name = __name__.split('.')[-3]

            # was succesfully saved, now, create directory for it
            # ./static/css/[app_name]/[typename]
            # ./static/js/[app_name]/[typename]
            # ./[app_name]/views/[typename].py
            os.mkdir('%s/static/css/%s/%s' % (settings.APP_DIR, app_name, self.name)
            os.mkdir('%s/static/js/%s/%s' % (settings.APP_DIR, app_name, self.name)

            fh = open('%s/%s/views/%s.py' % (settings.APP_DIR, app_name, self.name))
            fh.close()


    def getModel(self):
        return dbload.get_model("Viewer", self.name)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        app_label = "Viewer"

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

    def __unicode__(self):
        return self.name

    def getMappedItems(self):
        # TODO get child class and do stuff with it?
        raise NotImplementedError, "getMappedItems was not implemented in the base class"

    class Meta:
        app_label = "Viewer"

