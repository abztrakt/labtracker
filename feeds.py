from django.contrib.syndication.feeds import Feed
from labtracker.IssueTracker.models import Issue
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import feedgenerator
from django.http import HttpResponse

class LatestIssues(Feed):
    title = "Labtracker: Latest Issues"
    link = "/issues/all/"
    description = "The latest issues on Labtracker, a tool for managing LST learning spaces"

    def item_link(self, obj):
        return "http://crushinator.eplt.washington.edu:8080/issue/%d/" % obj.pk

    def author_name(self, obj):
        pass  

    def items(self, assignee):
        return Issue.objects.filter(assignee=assignee).order_by('-post_time')[:5]

def issues(request, assignee):
    feed = feedgenerator.Rss201rev2Feed(
                title=u'Labtracker: Latest Issues',
                link=u'/issues/all',
                description = u'The latest issues on Labtracker, a tool for managing LST learning spaces',
                language = u'en')
    #for issue in Issue.objects.filter(assignee=assignee).order_by('-post_time')[:5]:
    user = get_object_or_404(User, username=assignee) 
    for issue in Issue.objects.filter(assignee=user).order_by('-post_time')[:5]:
        feed.add_item(
                title=unicode(issue.title),
                link=u'http://crushinator.eplt.washington.edu:8080/issues/all/',
                description=unicode(issue.description))

    resp = HttpResponse(mimetype='application/rss+xml')

    feed.write(resp, 'utf8')
    return resp

