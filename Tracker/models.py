from django.db import models
from LabtrackerCore.models import Item

# Create your models here.
class Statistics(models.Model):
    login_time = models.DateTimeField(verbose_name='Login Time')
    logout_time = models.DateTimeField(null=True, verbose_name='Logout Time')
    ping_time = models.DateTimeField(null=True, verbose_name='Ping Time')
    item = models.ForeignKey(Item, verbose_name='Item Name')
    netid = models.CharField(max_length=20, verbose_name='UW Net ID')
    #regid = models.CharField(max_length=32, verbose_name='UW Reg ID')
