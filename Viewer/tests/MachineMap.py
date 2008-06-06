import random

from django.test.client import Client
from django.contrib.auth.models import User, check_password
from django.test import TestCase

import LabtrackerCore.models as c_models
import Machine.models as m_models
import Viewer.models as v_models

class MachineMapTest(TestCase):
    fixtures = ['test',]

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testShouldCreateMap(self):
        count = v_models.MachineMap.MachineMap.objects.count()
        mm = v_models.MachineMap.MachineMap(
                name = "testmap",
                shortname = "testmap",
                description = "desc"
            )

        mm.save()

        self.assertTrue(count < v_models.MachineMap.MachineMap.objects.count())

        # create a MachineMap and associate groups to it
        group = m_models.Group.objects.all()[0]
        self.assertTrue(group.items.count() > 0)

        mm.groups.add(group)
        mm.save()

        self.assertEquals(mm.groups.count(), 1)

class MachineMapWebTest(TestCase):
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

        for group in groups:
            self.map.groups.add(group) 

    def tearDown(self):
        """
        delete the user
        """
        self.user.delete()

    def testShouldModifyMap(self):
        """
        Try to modify the map that was created
        """

        r = random.Random()
        r.seed()

        self.client.login(username=self.user.username, password=self.password)

        unmapped_items = self.map.getUnmappedItems()
        old_count = len(unmapped_items)

        # map half the items
        items_to_map = unmapped_items[0:len(unmapped_items)/2]

        mm_obj = v_models.MachineMap.MachineMap


        req_data = {
                'save': 1,
                'map': [item.pk for item in items_to_map]
            }

        size = v_models.MachineMap.MachineMap_Size.objects.all()[0]

        # for each of the items to map, give them position and sizes and stuff
        for item in items_to_map:
            key = 'map[%s][%%s]' % (item.pk)
            req_data[key % 'x'] = r.randint(0, 1000)
            req_data[key % 'y'] = r.randint(0, 1000)
            req_data[key % 'size'] = size.name
            req_data[key % 'orient'] = ('H', 'V')[r.randint(0,1)]

        # map a few items
        response = self.client.post('/view/MachineMap/%s/modify' % self.map.shortname, req_data)
        self.assertContains(response, 'status', status_code=200)

        self.map = v_models.MachineMap.MachineMap.objects.get(pk=self.map.pk)

        print "\n%d : %d\n" % (len(items_to_map), self.map.getMappedItems().count())

        self.assertTrue(len(items_to_map) == self.map.getMappedItems().count())

