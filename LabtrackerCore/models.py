from django.db import models,connection

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
    inv_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60, unique=True)
    namespace = models.CharField(maxlength=60, unique=True)
    description = models.CharField(maxlength=2616)

    def __str__(self):
        return self.name

    class Admin:
        pass

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    it = models.ForeignKey(InventoryType)

    def __str__(self):
        """
        Will take the actual item name from whatever the Namespace_namespace
        """
        cursor = connection.cursor()
        namespace = self.it.namespace
        query = "SELECT name FROM %s_%s WHERE item_id=%%s" % (namespace,namespace.lower())
        cursor.execute(query, [self.item_id,])
        row = cursor.fetchone()
        return row[0]

class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    it = models.ForeignKey(InventoryType)

    def __str__(self):
        cursor = connection.cursor()
        namespace = self.it.namespace
        query = "SELECT name FROM %s_group WHERE group_id=%%s" % (namespace)
        cursor.execute(query, [self.group_id,])
        row = cursor.fetchone()
        return row[0]


class ViewType(models.Model):
    vt_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60, unique=True)
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

