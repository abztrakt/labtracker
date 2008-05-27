from django.db import models 

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


