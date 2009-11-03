from django import forms
import Viewer.models as vm

class TimeForm(forms.Form):
    time_start = forms.DateTimeField()
    time_end = forms.DateTimeField()
    cache_interval = forms.BooleanField(required=False)
    tags = forms.ModelMultipleChoiceField(queryset=vm.Tags.objects.all(), help_text="Select one or more tags", required=False)
    description = forms.CharField(required=False)
