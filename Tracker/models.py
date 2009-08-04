from django.db import models
from LabtrackerCore.models import Item

# Create your models here.
class Statistics(models.Model):
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(auto_now=True, null=True, verbose_name='Logout Time')
    item = models.ForeignKey(Item, verbose_name='Item Name')
    netid = models.CharField(max_length=20, verbose_name='UW Net ID')
    #regid = models.CharField(max_length=32, verbose_name='UW Reg ID')
