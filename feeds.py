from labtracker.IssueTracker.models import Issue
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import feedgenerator
from django.http import HttpResponse

def issues(request, assignee):
    """
    Given a username returns the latest 5 tickets in RSS format
    """
    user = get_object_or_404(User, username=assignee) 

    feed = feedgenerator.Rss201rev2Feed(
                title=u'Labtracker: Latest issues for %s' % assignee,
                link=u'/issues/all',
                description=u'The latest issues on Labtracker, a tool for managing LST learning spaces',
                language=u'en')

    for issue in Issue.objects.filter(assignee=user).order_by('-post_time')[:5]:
        feed.add_item(
                title=unicode(issue.title),
                link=u'http://crushinator.eplt.washington.edu:8080/issue/%d/' % issue.pk,
                description=unicode(issue.description))

    resp = HttpResponse(mimetype='application/rss+xml')

    feed.write(resp, 'utf8')
    return resp

