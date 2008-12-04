import django.forms as forms

import models

class itemStatusForm(forms.Form):
    """
    This form is used for setting the statuses for a Machine Item
    """

    status = forms.MultipleChoiceField(choices=\
        [(s.pk, s.name) \
             for s in models.Status.objects.all() if s.name != "Inuse"
        ])

    def _saveGroup(self, group):
        return False

    def _saveMachine(self, machine):
        statuses = models.Status.objects.in_bulk(self.cleaned_data['status'])
        for v in statuses.values():
            machine.status.add(v)

        return True

    def save(self, machine=None, group=None):
        """
        Update the given instance with the new statuses, should add on, not 
        remove, instance is the instance of the issue
        """

        if machine != None:
            return self._saveMachine(machine)
        elif group != None:
            return self._saveGroup(group)

        return False

