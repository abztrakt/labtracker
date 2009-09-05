from django.db import models
from LabtrackerCore.models import Item
from Machine.models import Location

# Create your models here.
class Statistics(models.Model):
    login_time = models.DateTimeField(verbose_name='Login Time')
    logout_time = models.DateTimeField(null=True, verbose_name='Logout Time')
    ping_time = models.DateTimeField(null=True, verbose_name='Ping Time')
    session_time = models.DecimalField(max_digits=16, decimal_places=2, null=True, verbose_name='Session Time')
    item = models.ForeignKey(Item, verbose_name='Item Name')
    netid = models.CharField(max_length=20, verbose_name='UW Net ID')
    #regid = models.CharField(max_length=32, verbose_name='UW Reg ID')

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
