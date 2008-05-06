from django import newforms as forms

from IssueTracker.models import *
import LabtrackerCore.models as LabtrackerCore

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

def createGroupList(inv_ids, field='Group'):
    list = {}

    for inv_id in inv_ids:
        # fetch groups with that invtype
        groups = LabtrackerCore.Group.objects.filter(it=inv_id)

        for group in groups:
            data = forms.models.model_to_dict(group.group)
            data['name'] = group.name
            list[group.group.group_id] = data
    return list

def createItemList(items, field='Item'):
    list = {}

    for item in items:
        data = forms.models.model_to_dict(item.item)
        data['name'] = item.name
        list[item.item.item_id] = data

    return list
