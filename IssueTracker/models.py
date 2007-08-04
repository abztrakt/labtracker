from django.db import models
from labtracker.LabtrackerCore.models import Item,InventoryType,Group
from django.contrib.auth.models import User

class ResolveState(models.Model):
    rs_id = models.AutoField(primary_key=True)
    name = models.CharField(maxlength=60)
    description = models.CharField(maxlength=2616)

    def __str__(self):
        return self.name

    class Admin:
        pass

class ProblemType(models.Model):
    pb_id = models.AutoField(primary_key=True)
    inv = models.ManyToManyField(InventoryType)
    name = models.CharField(maxlength=60, unique=True)
    description = models.CharField(maxlength=2616)

    def __str__(self):
        return self.name

    class Admin:
        pass

class Issue(models.Model):
    """
    Issues can be related to specific items or the whole InventoryType.
    Therefore, item_id is null=True
    """
    issue_id = models.AutoField(primary_key=True)
    it = models.ForeignKey(InventoryType, verbose_name="Inventory Type")
    group = models.ForeignKey(Group, null=True)
    item = models.ForeignKey(Item, null=True)

    reporter = models.ForeignKey(User, related_name='reporter')
    assignee = models.ForeignKey(User, related_name='assignee', null=True)
    cc = models.ManyToManyField(User, related_name="cc_user", null=True, 
            db_table="IssueTracker_email_cc")
    problem_type = models.ManyToManyField(ProblemType, null=True)
    post_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    resolve_time = models.DateTimeField(null=True)
    resolved_state = models.ForeignKey(ResolveState, null=True)
    title = models.CharField(maxlength=60)
    description = models.TextField()

    class Meta:
        permissions = (("can_modify_other", "Can modify anybody's posts"),
                    ("can_delete_other", "Can delete anybody's posts"),
                    ("can_view", "Can view issues"),)

    class Admin:
        pass

class IssuePost(models.Model):
    ip_id = models.AutoField(primary_key=True)
    issue = models.ForeignKey(Issue)
    user = models.ForeignKey(User)
    post_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Admin:
        pass;
