from labtracker.IssueTracker.models import *

def updateHistory(user, issue, msg):
    history = IssueHistory(user=user,message=msg,issue=issue)
    history.save()

def modelsToDicts(items):
    """
    Takes a list of items and turns each one into a dict, then returns the list of dicts
    """
    list = []
    for item in items:
        list.append(forms.models.model_to_dict( item ))
    return list
