from django.db import models

# Create your models here.
class Statistics(models.Model):
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(auto_now=True, null=True, verbose_name='Logout Time')
    mac1 = models.CharField(max_length=17, verbose_name='MAC Address')
    netid = models.CharField(max_length=20, verbose_name='UW Net ID')
    #regid = models.CharField(max_length=32, verbose_name='UW Reg ID')
