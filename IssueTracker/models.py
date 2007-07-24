from django.db import models
from labtracker.LabtrackerCore.models import Item,InventoryType
from django.contrib.auth.models import User

# TODO Hook up with the django permissions tables

class Issue(models.Model):
    """
    Issues can be related to specific items or the whole InventoryType.
    Therefore, item_id is null=True
    """
    issue_id = models.AutoField(primary_key=True)
    it = models.ForeignKey(InventoryType)
    item = models.ForeignKey(Item, null=True)

    user = models.ForeignKey(User)

    post_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    resolve_time = models.DateTimeField(null=True)
    name = models.CharField(maxlength=60)
    description = models.TextField()

class IssuePost(models.Model):
    ip_id = models.AutoField(primary_key=True)
    issue = models.ForeignKey(Issue)

    user = models.ForeignKey(User)

    post_date = models.DateTimeField(auto_now_add=True)
