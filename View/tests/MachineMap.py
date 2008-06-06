from django.test.client import Client
from django.contrib.auth.models import User, check_password
from django.test import TestCase

import LabtrackerCore.models as c_models
import Machine.models as m_models
import View.models as v_models

class MachineMapTest(TestCase):
    fixtures = ['test',]

    def setUp(self):
        """
        Creates test user and test issue
        """
        # create test user
        self.password = 't3$tu$ser'
        self.user = User.objects.create_user('testuser', 'test@example.com', self.password)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()


        # create a map
        groups = m_models.Group.objects.all()[0:2]
        self.map = v_models.MachineMap.MachineMap(name = 'testmap',
                shortname = 'testmap',
                description = "description")
        self.map.save()

        self.map.groups.add(groups)



    def tearDown(self):
        """
        delete the user
        """
        self.user.delete()

    def testShouldModifyMap(self):
        """
        Try to modify the map that was created
        """
        self.client.login(username=self.user.username, password=self.password)

        unmapped_items = self.map.getUnmappedItems()

        # map a few items
        rseponse = self.client.post('/view/MachineMap/%s/modify' % self.map.shortname, {
                'save': 1,
                'map': [item.id for item in unmapped_items]
            })
