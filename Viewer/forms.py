from django import forms
import Viewer.models as vm
from django.contrib.admin import widgets as cw

class TimeForm(forms.Form):
    time_start = forms.DateTimeField(widget=cw.AdminSplitDateTime)
    time_end = forms.DateTimeField(widget=cw.AdminSplitDateTime)
    cache_interval = forms.BooleanField(required=False)
    tags = forms.ModelMultipleChoiceField(queryset=vm.Tags.objects.all(), required=False)
    description = forms.CharField(required=False)

class FileTimeForm(forms.Form):
    time_start = forms.DateTimeField(widget=cw.AdminSplitDateTime)
    time_end = forms.DateTimeField(widget=cw.AdminSplitDateTime)
    
