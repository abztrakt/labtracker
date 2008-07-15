from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, check_password

from LabtrackerCore.models import Item, InventoryType, Group 
import LabtrackerCore.models as coreModels
import Machine.models as mModels
import IssueTracker.models as iModels
import IssueTracker.Email as Email


class IssueCreationTest(TestCase):
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

    def testLogin(self):
        """
        Logs in our test user and makes sure a success code is returned
        """
        response = self.client.post('/login/', 
                                    {'username' : 'testuser',
                                     'password' : 't3$tu$ser'})
        
        # successful login should send us to issues
        self.failUnlessEqual(response.status_code, 302)
        
    def testCreateIssue(self): 
        """
        Grabs the issue that was previously created and makes 
        sure it has the correct values
        """
        self.client.login(username=self.user.username, password=self.password)

        issues = iModels.Issue.objects.all()
        num_issues = issues.count()
        
        last_pk = 0
        if num_issues > 0:
            last_pk = issues.reverse()[0].pk

        title = "Everything is broken"
        response = self.client.post('/issue/new/', {
                'title':        title,
                'it':           coreModels.InventoryType.objects.all()[0].pk,
                'description':  "All the machines in the lab are broken. (knock on wood)"
            })

        self.failUnlessEqual(num_issues + 1, iModels.Issue.objects.all().count())

        issue = iModels.Issue.objects.filter(title=title).reverse()[0]
        self.issue = issue

        # make sure that the issue was created
        self.assertTrue(last_pk < issue.pk)

        self.failUnlessEqual(response.status_code, 302)
        self.assertRedirects(response, '/issue/%d/' % (self.issue.pk), status_code=302, target_status_code=200)

        # now make sure that we can actually view that issue
        response = self.client.get('/issue/%d/' % (self.issue.pk))

        self.assertTemplateUsed(response, "IssueTracker/view.html")
        self.assertContains(response, '<h2 id="title">%s</h2>' % (self.issue.title), status_code=200)


class PasswordChangeTest(TestCase):
    def setUp(self):
        """
        Create user
        """
        self.user = User.objects.create_user('testuser', 'test@example', 'supersecret')
        self.user.save()

    def testChangePassword(self):
        """
        Change the password and make sure it works
        """
        
        self.usertest = User.objects.get(username='testuser')

        response = self.client.post('/login/',
                         {'username' : 'testuser',
                          'password' : 'supersecret'})

        self.assertTrue(response) # logged in successfully
        
        # change password
        passwd = 'unit tests' 
        self.usertest.password = passwd 
        self.usertest.save()

        self.client.logout()

        # make sure the password was changed by trying
        # to login with the new password
        response = self.client.post('/login/',
                         {'username' : 'testuser',
                          'password' : 'unit tests'})

        self.assertTrue(response)

        response = self.client.post('/pref/pwchange/',
                                    {'old_password' : 'unit tests',
                                     'new_password1' : 'supersecret',
                                     'new_password2' : 'supersecret'})

        self.assertEquals(response.status_code, 302)

        response = self.client.post('/login/',
                         {'username' : 'testuser',
                          'password' : 'supersecret'})

        self.assertTrue(response)

class EmailTest(TestCase):
    def setUp(self):
        self.email = Email.Email()

    def testSending(self):
        self.email.appendSection(Email.EmailSection('Header', 'Content'))
        self.email.subject = 'subject'
        # to must be list
        self.email.to = [settings.EMAIL_TEST_RECIPIENT]
        self.email.send()

        # TODO make sure that it was sent?
