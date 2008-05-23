from django.newforms import ModelForm
from django.contrib.auth.models import User

import LabtrackerCore.models as coreModels

class BaseItemForm(ModelForm):
    class Meta:
        model = coreModels.Item
        fields = ('name')

class BaseGroupForm(ModelForm):
    class Meta:
        model = coreModels.Group
        fields = ('name', 'description', 'item')

class EmailForm(ModelForm):
    class Meta:
        model = User
        fields = ('email')
