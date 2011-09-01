from django import forms
import Viewer.models as vm

class TimeForm(forms.Form):
    time_start = forms.DateTimeField()
    time_end = forms.DateTimeField()
    cache_interval = forms.BooleanField(required=False)
    max_threshold = forms.FloatField(required=False,initial=12.0, label='Max threshold for data (in hours, optional)')
    #tags = forms.ModelMultipleChoiceField(queryset=vm.Tags.objects.all(), required=False)
    #description = forms.CharField(required=False)

class FileTimeForm(forms.Form):
    time_start = forms.DateTimeField()
    time_end = forms.DateTimeField()
    max_threshold = forms.FloatField(required=False,initial=12.0, label='Max threshold for data (in hours, optional)') 
