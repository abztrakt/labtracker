from django.db import models
from labtracker.LabtrackerCore.models import Item, LabUser, InventoryType, Group as SGroup
from django.contrib.auth.models import User

NAMESPACE = 'Machine'

def getInventoryType(self=None):
    it = InventoryType.objects.filter(namespace=NAMESPACE)[0]
    return it

class Status(models.Model):
    ms_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60, unique=True)
    inuse = models.BooleanField(default=False)
    usable = models.BooleanField(default=True)
    broken = models.BooleanField(default=False)

    def __unicode__(self):
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
    name = models.CharField(maxlength=60, unique=True)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

class Type(models.Model):
    mt_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60, unique=True)
    platform = models.ForeignKey(Platform)
    #it = models.ForeignKey(InventoryType, verbose_name='Inventory Type')
    model_name = models.CharField(maxlength=60)
    specs = models.TextField()
    purchase_date = models.DateField(null=True)
    warranty_date = models.DateField(null=True)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

class Location(models.Model):
    ml_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60, unique=True)
    building = models.CharField(maxlength=60, null=True)
    floor = models.SmallIntegerField(null=True)
    room = models.CharField(maxlength=30, null=True)
    comment = models.CharField(maxlength=600)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

class Machine(models.Model):
    item = models.OneToOneField(Item, editable=False, primary_key=True)
    mt = models.ForeignKey(Type, verbose_name='Machine Type')
    ms = models.ForeignKey(Status, verbose_name='Machine Status')
    ml = models.ForeignKey(Location, verbose_name='Location')
    name = models.CharField(maxlength=60, unique=True)
    ip = models.IPAddressField(verbose_name="IP Address")
    mac = models.CharField(maxlength=17, verbose_name='MAC Address')
    date_added = models.DateTimeField(auto_now_add=True)

    # XXX: what does manu_tag entail?
    manu_tag = models.CharField(maxlength=200, verbose_name="Manufacturers tag")
    comment = models.CharField(maxlength=400, blank=True)

    def __unicode__(self):
        return self.name

    def delete(self):
        self.item.delete()
        super(Machine,self).delete()

    def save(self):
        # first insert a new thing into Items
        try:
            self.item
        except:
            self.item = Item.objects.create(it = getInventoryType())
        super(Machine,self).save()

    class Admin:
        fields = (
           (None, {
                'fields': ('name','mt','ms','ml','ip','mac','manu_tag','comment'),
            }),
        )
        list_display = ('name','mt','ms','ml','ip','mac','date_added','manu_tag')
        search_fields = ['name','ip','mac']
        list_filter = ['mt','ms','date_added']

class Group(models.Model):
    group = models.ForeignKey(SGroup, editable=False, unique=True)
    name = models.CharField(maxlength=60, unique=True)
    machines = models.ManyToManyField(Machine, null=True)
    is_lab = models.BooleanField()
    casting_server = models.IPAddressField()
    gateway = models.IPAddressField()
    description = models.CharField(maxlength=2616)

    def __unicode__(self):
        return self.name

    def delete(self):
        self.group.delete()
        super(Group,self).delete()

    def save(self):
        try:
           self.group
        except:
           self.group = SGroup.objects.create(it = getInventoryType())
        super(Group,self).save()

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

    def __unicode__(self):
        extra = ""
        if self.is_primary:
            extra = " (Primary)"
        return "%s - %s%s" % (self.mg, self.user, extra)
