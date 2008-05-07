from django.test import TestCase
from django.contrib.auth.models import User
from IssueTracker.models import Issue
from LabtrackerCore.models import Item, InventoryType, Group 

class IssueCreationTest(TestCase):
    def setUp(self):
        """
        """
        # create test user
        self.user = User.objects.create_user('testuser', 'test@example.com', 't3$tu$ser')
        self.user.save()

        # create test issue
        self.issue = Issue(reporter=self.user,title="Everything is broken", description="All the machines in the lab are broken. (knock on wood)")
        self.issue.save()
        self.issueId = self.issue.issue_id

    def testLogin(self):
        response = self.client.post('/issue/login/', 
                                    {'username' : 'testuser',
                                     'password' : 't3$tu$ser'})
            
        self.assertEquals(response.status_code, 200)
        
    def testCreateIssue(self): 
        # make sure it's there and has the right values
        self.testissue = Issue.objects.get(issue_id=self.issueId)

        self.assertEquals(self.issue.title, self.testissue.title)
        self.assertEquals(self.issue.description, self.testissue.description)
        self.assertEquals(self.issue.reporter, self.user)
    
    def testUpdateIssue(self):
        self.issue.title = "erry thang is broke"
        self.issue.save()

        self.testissue = Issue.objects.get(issue_id=self.issueId)

        self.assertEquals(self.issue.title, self.testissue.title)
