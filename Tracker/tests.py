from hashlib import md5

from django.test import TestCase
from django.http import HttpRequest, QueryDict
from django.core.urlresolvers import reverse

from Machine import models as mm
from LabtrackerCore import models as cm
import models as tm

class TrackerMachineUpdate(TestCase):
    fixtures = ['dev',]

    def setUp(self):
        """
        Create a new machine to test with
        """
        self.m = mm.Item(
            name = "test_machine_item",
            location = mm.Location.objects.all()[0],
            type = mm.Type.objects.all()[0],
            ip = "192.168.2.200",
            mac1 = "00:1b:b9:db:25:3d",
            wall_port = "12za3",
            manu_tag = "test",
            uw_tag = "test",
        )
        self.m.save()

        # create a new user
        self.username = "bobm"

    def tearDown(self):
        """
        Delete the machine
        """
        self.m.delete()

    def testUpdate(self):
        """
        Try a post to update machine
        """

        # make sure that the entry doesn't exist yet
        md5name = md5(self.username).hexdigest()

        user = cm.LabUser.objects.filter(user_id = md5name)
        self.assertEqual(0, user.count())

        # attempt an update
        resp = self.client.post(reverse('tracker-machine', 
                                        kwargs= {'name': self.m.name,}), 
                                { 'user': self.username, 'status': 'login', })

        print resp.content

        self.assertContains(resp, "Inuse")



