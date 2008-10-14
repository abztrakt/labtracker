from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User, check_password

import LabtrackerCore.models as models

class LabtrackerTest(TestCase):
    fixtures = ['dev',]

    def setUp(self):
        # create test user
        self.password = 't3$tu$ser'
        self.user = User.objects.create_user('testuser', 'test@example.com', 
                self.password)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

    def testShouldChangePassword(self):
        """
        Change the password
        """
        self.client.login(username=self.user.username, password=self.password)

        # attempt to get the password change form

        url = reverse('pwchange')
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pwchange.html")

        pw = "newpassword"
        # post to pwchange
        response = self.client.post(url,
                {
                    'old_password': self.password,
                    'new_password1': pw,
                    'new_password2': pw
                })

        self.assertTrue(response.status_code == 302)

        self.client.logout()

        response = self.client.post(reverse('login'), 
                {'username' : self.user.username, 'password' : pw})

        self.failUnlessEqual(response.status_code, 302)


