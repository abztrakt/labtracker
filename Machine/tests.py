from django.test import TestCase
from django.http import HttpRequest, QueryDict

import forms
import models

class MachineIssue(TestCase):
    fixtures = ['dev',]

    def setUp(self):
        pass

    def testSingleUpdateForm(self):
        """
        Test the itemStatusForm to see if it updates the machine correctly
        """

        qdict = QueryDict("", mutable=True)
        qdict.setlist('status', ['2'])
        form = forms.itemStatusForm(qdict)

        self.assertTrue(form.is_valid())

        # get machine
        machine = models.Item.objects.get(pk=1)
        num_status = machine.status.all().count()

        self.assertEquals(num_status, 2)

        form.save(machine)

        self.assertEquals(machine.status.all().count(), num_status+1)
