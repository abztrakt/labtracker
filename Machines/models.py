from django.db import models
from labtracker.LabtrackerCore.models import Item,LabUser,InventoryType
from django.contrib.auth.models import User

class Status(models.Model):
    ms_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60)
    inuse = models.BooleanField(default=False)
    usable = models.BooleanField(default=True)
    broken = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="Status"

    class Admin:
        list_display = ('name','inuse','usable','broken')
        fields = (
            (None, {'fields': ('name', ('inuse','usable','broken',))}),
        )

class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60)

    def __str__(self):
        return self.name

    class Admin:
        pass

class Type(models.Model):
    mt_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60)
    platform = models.ForeignKey(Platform)
    it = models.ForeignKey(InventoryType, verbose_name='Inventory Type')
    model_name = models.CharField(maxlength=60)
    specs = models.TextField()
    purchase_date = models.DateField(null=True)
    warranty_date = models.DateField(null=True)

    def __str__(self):
        return self.name

    class Admin:
        pass

class Machine(models.Model):
    machine_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item)
    mt = models.ForeignKey(Type, verbose_name='Machine Type')
    ms = models.ForeignKey(Status, verbose_name='Machine Status')
    name = models.CharField(maxlength=60)
    ip = models.IPAddressField(verbose_name="IP Address")
    mac = models.CharField(maxlength=17, verbose_name='MAC Address')

    # XXX: look more into the manu_tag and what it would require
    manu_tag = models.CharField(maxlength=200)

    def __str__(self):
        return self.name

    class Admin:
        pass

class Group(models.Model):
    mg_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60)
    machines = models.ManyToManyField(Machine, null=True)
    is_lab = models.BooleanField()
    casting_server = models.IPAddressField()
    gateway = models.IPAddressField()
    description = models.CharField(maxlength=2616)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name','is_lab','casting_server','gateway')

class History(models.Model):
    mh_id = models.AutoField(primary_key=True)
    machine = models.ForeignKey(Machine)
    ms = models.ForeignKey(Status)
    user = models.ForeignKey(LabUser)
    time = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    mg = models.ForeignKey(Group, edit_inline=models.TABULAR,num_in_admin=2)

    user = models.ForeignKey(User,core=True)
    is_primary = models.BooleanField(core=True,default=False)

    def __str__(self):
        extra = ""
        if self.is_primary:
            extra = " (Primary)"
        return "%s - %s%s" % (self.mg, self.user, extra)
