from django.newforms import ModelForm
from LabtrackerCore.models import *

class BaseItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name')

class BaseGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description', 'item')
