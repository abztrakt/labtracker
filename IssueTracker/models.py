from datetime import datetime
from django.db import models
from LabtrackerCore.models import Item,InventoryType,Group
from django.contrib.auth.models import User
from django.test import TestCase

class ResolveState(models.Model):
    """
    Issues are resolved into a resolve state such as this
    """

    rs_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=400)

    def __unicode__(self):
        return self.name

class ProblemType(models.Model):
    """
    Issues have mulitple probme types associated to them
    """

    pb_id = models.AutoField(primary_key=True)
    inv = models.ManyToManyField(InventoryType, blank=True, null=True)
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=400)

    def __unicode__(self):
        return self.name

class Issue(models.Model):
    """
    Issues can be related to specific items or the whole InventoryType.
    Therefore, item_id is null=True
    """

    issue_id = models.AutoField(primary_key=True, editable=False)

    it = models.ForeignKey(InventoryType, verbose_name="Inventory Type", blank=True,
            null=True)
    group = models.ForeignKey(Group, null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True)
    reporter = models.ForeignKey(User, related_name='reporter')

    assignee = models.ForeignKey(User, related_name='assignee', null=True, 
            blank=True)
    cc = models.ManyToManyField(User, related_name="cc_user", null=True, 
            blank=True, verbose_name="CC", db_table="IssueTracker_email_cc")
    problem_type = models.ManyToManyField(ProblemType, null=True, blank=True,
            help_text="Select one or more problems.", verbose_name="problems")
    post_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    resolve_time = models.DateTimeField(null=True, blank=True)
    resolved_state = models.ForeignKey(ResolveState, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def save(self, *args, **kwargs):
        # check to see if the resolved_state has changed, if so, then change 
        # resolve_time
        if self.pk:
            old = Issue.objects.get(pk=self.pk)

            if old.resolved_state != self.resolved_state:
                self.resolve_time = datetime.now()

        super(Issue, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%d - %s" % (self.issue_id, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('IssueTracker.views.viewIssue', [str(self.issue_id)])


    class Meta:
        permissions = (("can_modify_other", "Can modify anybody's posts"),
                    ("can_delete_other", "Can delete anybody's posts"),
                    ("can_view", "Can view issues"),)

class IssueHistory(models.Model):
    """
    Basically, keeps track of some of the changes made to a model outside of 
    the IssueComment area
    """

    ih_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    issue = models.ForeignKey(Issue)
    time = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=300)

class IssueComment(models.Model):
    """
    This is for the comments people add to each issues
    """

    ip_id = models.AutoField(primary_key=True)
    issue = models.ForeignKey(Issue)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=False)

"""
Test Cases
"""
class NullForeignKeyTest(TestCase):
    """
    When sorting by a nullable foreign key, rows with a null value would disappear
    """
    fixtures = ['dev']
    def testNullKey(self): 
        issues = Issue.objects.filter(resolved_state__isnull=True).order_by('-assignee')
        self.assertEquals(7, issues.count())


