from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User, check_password

from LabtrackerCore.models import Item, InventoryType, Group 
from IssueTracker.models import Issue
import IssueTracker.Email as Email


class IssueCreationTest(TestCase):
    def setUp(self):
        """
        Creates test user and test issue
        """
        # create test user
        self.user = User.objects.create_user('testuser', 'test@example.com', 't3$tu$ser')
        self.user.save()

        # create test issue
        self.issue = Issue( reporter=self.user, 
                            title="Everything is broken", 
                            description="All the machines in the lab are broken. (knock on wood)" )
        self.issue.save()
        self.issueId = self.issue.issue_id

    def testLogin(self):
        """
        Logs in our test user and makes sure a success code is returned
        """
        response = self.client.post('/login/', 
                                    {'username' : 'testuser',
                                     'password' : 't3$tu$ser'})
            
        self.assertEquals(response.status_code, 200)
        
    def testCreateIssue(self): 
        """
        Grabs the issue that was previously created and makes 
        sure it has the correct values
        """
        # make sure it's there and has the right values
        self.testissue = Issue.objects.get(issue_id=self.issueId)

        self.assertEquals(self.issue.title, self.testissue.title)
        self.assertEquals(self.issue.description, self.testissue.description)
        self.assertEquals(self.issue.reporter, self.user)
    
    def testUpdateIssue(self):
        """
        Grabs the previously created issue and updates it.  Then
        makes a change to it and grabs it, ensures that it is correct
        """
        self.issue.title = "erry thang is broke"
        self.issue.save()

        self.testissue = Issue.objects.get(issue_id=self.issueId)

        self.assertEquals(self.issue.title, self.testissue.title)

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
        self.email.to = settings.EMAIL_TEST_RECIPIENT
        self.email.send()

        # TODO make sure that it was sent?
