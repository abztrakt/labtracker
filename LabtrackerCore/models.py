"""
These are the Core models for Labtracker

"""

from django.db import models,connection
from django.core.exceptions import ImproperlyConfigured
import django.core.management as dman
import django.db.models.loading as dbload

import labtracker.settings as lset

# TODO, is this needed?
class LabUser(models.Model):
    """
    Not associated with the actually authenticated users, this only keeps track
    of users logging in/out of the computers. For a list of users for the auth
    list, please look at the django.contrib.auth.models
    """
    user_id = models.CharField(primary_key=True, max_length=32)

    def __unicode__(self):
        return self.user_name

class InventoryType(models.Model):
    """
    This holds all the Inventory Types. 
    E.g.: computer vs. scanner vs. projector
    """

    inv_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    namespace = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=2616)

    def __unicode__(self):
        return self.name

    def save(self):
        """
        On the creation of an InventoryType, create the project directory
        """

        # get the current directory
        import django.core.management.commands.startapp as startapp

        app_dir = dman.setup_environ(lset)              # get app_dir from settings
        app_c = startapp.ProjectCommand(app_dir)

        # TODO: Need to handle bad namespaces
        app_c.handle_label(str(self.namespace))         # construct
        super(InventoryType,self).save()

    def delete(self):
        """
        On deletion, kill the models
        """

        # delete the application and all it's related models
        import django.core.management.commands.sqlclear as sqlclear

        app_dir = dman.setup_environ(lset)
        try:
            app = dbload.get_app(self.namespace)
            # see if there are any models
            if len(dbload.get_models(app)) > 0:
                app_c = sqlclear.Command()
                app_c.handle(*[self.namespace,])

            # deletion of the folder should be left to the admin. as well as removal from
            # settings

        except ImproperlyConfigured, e:
            pass
        except Exception, e:
            print e[0]
            raise

        super(InventoryType,self).delete()

    class Admin:
        list_display = ('name','namespace','description')

class Item(models.Model):
    """
    Actual items, could be of any inventorytype
    """

    item_id = models.AutoField(primary_key=True)
    it = models.ForeignKey(InventoryType, editable=False)
    name = models.CharField(max_length=60, unique=True)

    def __unicode__(self):
        """
        Will take the actual item name from whatever the Namespace_namespace
        """
        return self.name

    class Admin:
        pass

class Group(models.Model):
    """
    Groups the items, can either by group of one inventorytype or all inventorytypes
    """

    group_id = models.AutoField(primary_key=True)
    it = models.ForeignKey(InventoryType, null=True, blank=True)
    name = models.CharField(max_length=60, unique=True, core=True)
    description = models.CharField(max_length=2616, core=True)

    item = models.ManyToManyField(Item, null=True, blank=True)

    def __unicode__(self):
        """
        Print out the name of the group
        """
        return self.name

    class Admin:
        pass

