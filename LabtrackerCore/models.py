from django.db import models

# TODO, is this needed?
class LabUser(models.Model):
    """
    Not associated with the actually authenticated users, this only keeps track
    of users logging in/out of the computers. For a list of users for the auth
    list, please look at the django.contrib.auth.models
    """
    user_id = models.AutoField(primary_key=True)

    # this will be a md5'd hash of actual user_name
    user_name = models.CharField(maxlength=32)

    def __str__(self):
        return self.user_name

class InventoryType(models.Model):
    it_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60)
    classname = models.CharField(maxlength=60, unique=True)
    description = models.CharField(maxlength=2616)

    def __str__(self):
        return self.name

    class Admin:
        pass

# Think about revamping this, is it really needed?
class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    it = models.ForeignKey(InventoryType)

    def __str__(self):
        return "%d (%s)" % (self.item_id, self.it);

    class Admin:
        pass

class ViewType(models.Model):
    vt_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60)
    description = models.CharField(maxlength=2616)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name','description')

class View(models.Model):
    view_id = models.AutoField(primary_key=True)
    vt = models.ForeignKey(ViewType, verbose_name="View Type")
    name = models.CharField(maxlength=60)
    url = models.URLField()
    description = models.CharField(maxlength=2616)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name','vt','url')

