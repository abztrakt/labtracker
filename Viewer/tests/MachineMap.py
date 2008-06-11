import random
import os

from django.conf import settings
from django.test.client import Client
from django.contrib.auth.models import User, check_password
from django.test import TestCase

import LabtrackerCore.models as c_models
import Machine.models as m_models
import Viewer.models as v_models

class MachineMapTest(TestCase):
    fixtures = ['dev',]

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
    fixtures = ['dev',]

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

        self.r = random.Random()
        self.r.seed()

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

        # delete the extra testmap folder
        os.rmdir('%s/static/css/Viewer/MachineMap/%s' % (settings.APP_DIR, self.map.name))

    def testShouldGetMap(self):
        """
        Should be able to view the map
        """

        response = self.client.get('/views/MachineMap/%s/' % (self.map.name))
        self.assertContains(response, self.map.name, status_code = 200)

        

    def testShouldModifyMap(self):
        """
        Try to modify the map that was created
        """

        print "\n\n================= testShouldModifyMap ======================"
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
        param_template = 'map[%s][%s]'
        for item in items_to_map:
            req_data[param_template % (item.pk, 'x')] = self.r.randint(0, 1000)
            req_data[param_template % (item.pk, 'y')] = self.r.randint(0, 1000)
            req_data[param_template % (item.pk, 'size')] = size.name
            req_data[param_template % (item.pk, 'orient')] = ('H', 'V')[self.r.randint(0,1)]

        print "request data: \n%s" % (req_data)

        # map a few items
        response = self.client.post('/views/MachineMap/%s/modify' % \
                self.map.shortname, req_data)

        self.assertContains(response, 'status', status_code=200)

        self.map = v_models.MachineMap.MachineMap.objects.get(pk=self.map.pk)

        req_num_items = len(items_to_map)
        actual_num_items = self.map.getMappedItems().count()

        print "Requested num to map: %d, was able to map: %d" % (req_num_items, actual_num_items)
        self.assertTrue(req_num_items == actual_num_items) 


        # change the position of one of the objects and make sure that only one new mapped item is added
        num_mapped_items = self.map.getMappedItems().count()
        item = items_to_map[0]
        pos_req_data = {
                'save': 1,
                'map': [item.pk]
            }
        pos_req_data[param_template % (item.pk, 'x')] = 0
        pos_req_data[param_template % (item.pk, 'y')] = 0
        response = self.client.post('/views/MachineMap/%s/modify' % \
                self.map.shortname, pos_req_data)
        self.assertContains(response, 'status', status_code=200)
        self.assertTrue(num_mapped_items == self.map.getMappedItems().count())

        # change the rotation of one of the objects and make sure that only one new mapped item is added
        old_orient = req_data[param_template % (item.pk, 'orient')]

        rot_req_data = {
                'save': 1,
                'map': [item.pk]
            }
        rot_req_data[param_template % (item.pk, 'orient')] = ('H', 'V')[old_orient == 'H']

        response = self.client.post('/views/MachineMap/%s/modify' % \
                self.map.shortname, rot_req_data)
        self.assertContains(response, 'status', status_code=200)

        self.assertTrue(num_mapped_items == self.map.getMappedItems().count())

        print "\n============================================================\n"



