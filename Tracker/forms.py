from django import forms

class TimeForm(forms.Form):
    time_start = forms.DateTimeField()
    time_end = forms.DateTimeField()

