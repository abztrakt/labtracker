import os

from django.db import models
from django.conf import settings
import django.db.models.loading as dbload
from django.test import TestCase

import LabtrackerCore.models as c_models
import Machine.models

class ViewType(models.Model):
    """
    Every type of view is registered here, referenced by Viewer
    """
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=2616)

    def save(self):
        # check if this is the first time this ViewType was created
        newtype = True if self.pk == None else False 

        super(ViewType, self).save()

        if newtype:
            app_name = __name__.split('.')[-3]

            # was succesfully saved, now, create directory for it
            # ./static/css/[app_name]/[typename]
            # ./static/img/[app_name]/[typename]
            # ./static/js/[app_name]/[typename]
            # ./[app_name]/views/[typename].py
            css_dir = '%s/static/css/%s/%s' % (settings.APP_DIR, app_name, self.name)
            img_dir = '%s/static/img/%s/%s' % (settings.APP_DIR, app_name, self.name)
            js_dir = '%s/static/js/%s/%s' % (settings.APP_DIR, app_name, self.name)

            for d in (css_dir, img_dir, js_dir):
                if not os.path.isdir(d):
                    os.mkdir(d)
                    
            for dir in ['views', 'models']:
                fh = open('%s/%s/%s/%s.py' % (settings.APP_DIR, app_name, dir, self.name), 'w')
                fh.close()

            fh = open('%s/%s/models/__init__.py' % (settings.APP_DIR, app_name), 'a')
            fh.write('import %s' % (self.name))
            fh.close()

    def delete(self):
        super(ViewType, self).delete()

        app_name = __name__.split('.')[-3]

        css_dir = '%s/static/css/%s/%s' % (settings.APP_DIR, app_name, self.name)
        img_dir = '%s/static/img/%s/%s' % (settings.APP_DIR, app_name, self.name)
        js_dir = '%s/static/js/%s/%s' % (settings.APP_DIR, app_name, self.name)

        for d in (css_dir, img_dir, js_dir):
            if os.path.exists(d):
                for f in os.listdir(d):
                    os.remove(f)
                os.rmdir(d)

        for dir in ['views', 'models']:
            path = '%s/%s/%s/%s.py' % (settings.APP_DIR, app_name, dir, self.name)
            os.remove(path)

        fh = open('%s/%s/models/__init__.py' % (settings.APP_DIR, app_name), 'r')
        lines = fh.readlines()
        fh.close()
        try:
            lines.remove('import %s' % (self.name))
        except ValueError, e:
            pass
       
        fh = open('%s/%s/models/__init__.py' % (settings.APP_DIR, app_name), 'w')
        fh.writelines(lines)
        fh.close()

    def getModel(self):
        return dbload.get_model("Viewer", self.name)

    def __unicode__(self):
        return self.name

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
    groups = models.ManyToManyField(c_models.Group)
            # TODO find new method for doing filter_interface
            #filter_interface=models.HORIZONTAL)
    type = models.ForeignKey(ViewType, editable=False)

    def __unicode__(self):
        return self.name

    def get_child(self):
        return getattr(self, self.type.name.lower())

    def getMappedItems(self):
        # TODO get child class and do stuff with it?
        raise NotImplementedError, "getMappedItems was not implemented in the base class"

    class Meta:
        app_label = "Viewer"


class ViewTypeTestCase(TestCase):
    """
    Tests the ViewType creation/deletion
    """
    name = 'TestType'

    def setUp(self):
        self.view_type = ViewType(name="%s" % self.name, description="This is a test type")
        self.view_type.save()

    def testCreateViewType(self):
        """
        Creates a ViewType and checks that all folders and files are created
        """
        app_name = __name__.split('.')[-3]

        css_dir = '%s/static/css/%s/%s' % (settings.APP_DIR, app_name, self.name)
        img_dir = '%s/static/img/%s/%s' % (settings.APP_DIR, app_name, self.name)
        js_dir = '%s/static/js/%s/%s' % (settings.APP_DIR, app_name, self.name)

        for d in (css_dir, img_dir, js_dir):
            self.failUnless(os.path.isdir(d))
                
        for dir in ['views', 'models']:
            path = '%s/%s/%s/%s.py' % (settings.APP_DIR, app_name, dir, self.name)
            self.failUnless(os.path.exists(path))

        fh = open('%s/%s/models/__init__.py' % (settings.APP_DIR, app_name), 'r')
        lines = fh.readlines()
        fh.close()
        self.failUnless('import %s' % self.name in lines)

        # deleting here instead of tear down because the 
        # delete test case deletes the ViewType first
        self.view_type.delete()

    def testDeleteViewType(self):
        """
        Ensures that the ViewType is totally deleted
        """
        self.view_type.delete()

        app_name = __name__.split('.')[-3]

        css_dir = '%s/static/css/%s/%s' % (settings.APP_DIR, app_name, self.name)
        img_dir = '%s/static/img/%s/%s' % (settings.APP_DIR, app_name, self.name)
        js_dir = '%s/static/js/%s/%s' % (settings.APP_DIR, app_name, self.name)

        for d in (css_dir, img_dir, js_dir):
            self.failUnless(not os.path.isdir(d))
                
        for dir in ['views', 'models']:
            path = '%s/%s/%s/%s.py' % (settings.APP_DIR, app_name, dir, self.name)
            self.failUnless(not os.path.exists(path))

        fh = open('%s/%s/models/__init__.py' % (settings.APP_DIR, app_name), 'r')
        lines = fh.readlines()
        fh.close()
        self.failUnless('import %s' % self.name not in lines)

