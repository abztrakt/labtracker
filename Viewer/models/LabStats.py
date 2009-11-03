from django.db import models
from django.conf import settings
from LabtrackerCore.models import Item
from Machine.models import Location

from labtracker.Viewer.models import base
import labtracker.Viewer.utils 

app_name = __name__.split('.')[-3]

class LabStats(base.ViewCore):
    view = models.OneToOneField(base.ViewCore, parent_link=True, editable=False)
    #XXX Does not follow DRY principle. Use URL resolver when possible.
    def get_absolute_url(self):
        return 'LabStats/'
    def get_absolute_edit_url(self):
        return 'LabStats/edit/'

    class Meta:
        app_label = "Viewer"

class Tags(models.Model):
    """
    Categorical tags for StatsCache row entries
    """
    id = models.AutoField(primary_key=True)
    name = models.SlugField(max_length=60, unique=True)
    description = models.CharField(max_length=400, blank=True)

    class Meta:
        app_label = "Viewer"

class StatsCache(models.Model):
    location = models.ForeignKey(Location, verbose_name='Location')
    time_start = models.DateField(verbose_name='Start of Week')
    time_end = models.DateField(verbose_name='End of Week')
    min_time = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='Minimum Seat Time in Minutes')
    max_time = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='Maximum Seat Time in Minutes')
    mean_time = models.FloatField(verbose_name='Average Seat Time in Minutes')
    stdev_time = models.FloatField(verbose_name='Standard Deviation Time in Minutes')
    total_time = models.DecimalField(max_digits=16, decimal_places=2, verbose_name='Total Seat Time in Minutes')
    total_items = models.IntegerField(verbose_name='Total Items in Location')
    total_logins = models.IntegerField(verbose_name='Total Logins in Location')
    total_distinct = models.IntegerField(verbose_name='Total Distinct Logins in Location')

    description = models.CharField(max_length=255, verbose_name='Description of Cached Interval')
    tags = models.ManyToManyField(Tags, verbose_name='Tags attached to Cached Interval')

    class Meta:
        app_label = "Viewer"
