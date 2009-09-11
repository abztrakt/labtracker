import socket
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
        self.ip = "192.168.2.134"
        self.m = mm.Item(
            name = "test_machine_item",
            location = mm.Location.objects.all()[0],
            type = mm.Type.objects.all()[0],
            ip = self.ip,
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
                                { 'user': self.username, 'status': 'login', },
                                REMOTE_ADDR=self.ip )

        self.assertContains(resp, "Inuse")

        # this update should fail
        resp = self.client.post(reverse('tracker-machine', 
                                        kwargs= {'name': self.m.name,}), 
                                { 'user': self.username, 'status': 'login', }, )

        self.failUnlessEqual(403, resp.status_code)

    def testTrack(self):
        """
	    Try processing a login/logout request
	    """

        # Process a login
        prev_count = tm.Statistics.objects.all().count()
        resp = self.client.post(reverse('track', kwargs= {'action': 'login', 'macs': self.m.mac1}), {'user': self.username, 'status': 'login'})

        stats = tm.Statistics.objects.all()

        self.assertEqual(stats.count(), prev_count + 1)
        self.failUnlessEqual(200, resp.status_code)
        self.assertContains(resp, "Inuse")
	
        # Process a logout
        prev_count = stats.count()
        resp = self.client.post(reverse('track', kwargs= {'action': 'logout', 'macs': self.m.mac1}), {'user': self.username, 'status': 'logout'})

        stats = tm.Statistics.objects.all()
        self.assertEqual(stats.count(), prev_count)
        self.failIfEqual(stats[0].logout_time, None)


