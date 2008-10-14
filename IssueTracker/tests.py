from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, check_password

import simplejson

from LabtrackerCore.models import Item, InventoryType, Group 
import LabtrackerCore.models as coreModels
import Machine.models as mModels
import IssueTracker.models as iModels
import IssueTracker.Email as Email

from datetime import datetime

class IssueCreationTest(TestCase):
    fixtures = ['dev',]

    def setUp(self):
        """
        Creates test user 
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
        response = self.client.post(reverse('login'), 
                {'username' : self.user.username, 'password' : self.password})
        
        # successful login should send us to issues
        self.failUnlessEqual(response.status_code, 302)

    def testAjaxGroups(self):
        """
        Grab the groups for Machines through the ajax interface
        """
        self.client.login(username=self.user.username, password=self.password)

        # first, see what groups are available for Machines
        inv_id = coreModels.InventoryType.objects.filter(name='Machine')[0].inv_id
        groups = set([m.name for m in mModels.Group.objects.all()])

        # when we fetch ajax for inv_id is 1, we *should* get all the groups
        url = reverse('IssueTracker.views.ajax.getGroups')
        response = self.client.post(url,
                { 'type': 'json', 'it_id': inv_id })

        self.failUnlessEqual(response.status_code, 200)

        # convert the response content to a python dict
        data = simplejson.JSONDecoder().decode(response.content)

        ret_groups = set([data[key]["name"] for key in data.keys()])
        self.assertTrue(len(ret_groups) > 0)
        self.assertEquals(len(groups.difference(ret_groups)), 0)

    def testAjaxItems(self):
        """
        Grab the items for Machine groups 'Empty Group' and 'Group1', ensure 
        they return correct items
        """
        self.client.login(username=self.user.username, password=self.password)

        # fetch the two groups
        groups = mModels.Group.objects.filter(name__in = ['Empty Group', 'Group1'])

        if groups[0].name == u'Empty Group':
            group_e = groups[0]
            group_1 = groups[1]
        else:
            group_1 = groups[0]
            group_e = groups[1]

        url = reverse('IssueTracker.views.ajax.getItems')

        def fetchJSON(group):
            response = self.client.post(url,
                { 'type': 'json', 'group_id': group.pk })

            self.failUnlessEqual(response.status_code, 200)

            # convert the response content to a python dict
            return simplejson.JSONDecoder().decode(response.content)


        # fetch for empty group first
        data = fetchJSON(group_e)
        self.failUnlessEqual(len(data), 0)

        # now do the group1
        data = fetchJSON(group_1)
        self.assertTrue(len(data) > 0)

        items = set([item.pk for item in group_1.items.all()])
        ret_items = set([data[key]["item_id"] for key in data.keys()])

        self.assertEquals(len(items.difference(ret_items)), 0)

        
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
        response = self.client.post(reverse('createIssue'), {
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
        self.assertRedirects(response, '/issue/%d/' % (self.issue.pk), 
                status_code=302, target_status_code=200)

        # now make sure that we can actually view that issue
        response = self.client.get(reverse('view', args=[self.issue.pk]))

        self.assertTemplateUsed(response, "view.html")
        self.assertContains(response, '<h2 id="title">%s</h2>' % (self.issue.title), status_code=200)

class PasswordChangeTest(TestCase):
    def setUp(self):
        """
        Create user
        """
        self.user = User.objects.create_user('testuser', 'test@example', 
                'supersecret')
        self.user.save()

    def testChangePassword(self):
        """
        Change the password and make sure it works
        """
        
        self.usertest = User.objects.get(username='testuser')

        response = self.client.post(reverse('login'),
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
        response = self.client.post(reverse('login'),
                         {'username' : 'testuser',
                          'password' : 'unit tests'})

        self.assertTrue(response)

        response = self.client.post(reverse('pwchange'),
                                    {'old_password' : 'unit tests',
                                     'new_password1' : 'supersecret',
                                     'new_password2' : 'supersecret'})

        self.assertEquals(response.status_code, 302)

        response = self.client.post(reverse('login'),
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

class UpdateIssueTest(TestCase):
    fixtures = ['dev',]

    def setUp(self):
        """
        Creates test user 
        """
        self.password = 't3$tu$ser'
        self.user = User.objects.create_user('testuser', 'test@example.com', self.password)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        self.issue = iModels.Issue.objects.get(pk=1)

    def tearDown(self):
        self.user.delete()

    def testUpdateIssue(self):
        """
        Tests adding/removing CC list, adding comment
        """
        self.client.post(reverse('login'),
                            {'username' : 'testuser',
                             'password' : 't3$tu$ser'})

        issueUser = self.issue.cc.get(username='zhaoz')
    
        self.client.get(reverse('IssueTracker-modIssue', args=[1]),
                            {'action': 'dropcc',
                            'user': issueUser.pk,
                            'js': 1})

        self.failUnless(self.issue.cc.filter(username=issueUser.username).count()==0)

        self.client.get(reverse('IssueTracker-modIssue', args=[1]),
                            {'action': 'addcc',
                            'user': self.user.username,
                            'js': 1})

        self.failUnless(self.issue.cc.filter(username=self.user.username).count()==1)

        self.client.post(reverse('IssueTracker-update', args=[1]),
                        {   'issue': self.issue.pk,
                            'user': issueUser, 
                            'comment': 'here is a test comment'
                        })

        comment = iModels.IssueComment.objects.get(issue=self.issue)
        self.failUnless(comment is not None)

    def testChangeAssignee(self):
        """
        Tests changing the assignee of an issue
        """
        # FIXME can't get this to change assignee
        """
        issue = iModels.Issue.objects.get(pk=3)
        #comment = iModels.IssueComment.objects.get(issue=issue)


        self.client.post('/issue/3/post/', 
                    {
                        'assignee'          : 1,
                        'resolved_state'    : '',
                        'comment'           : '',
                        'problem_type'      : issue.problem_type.values()[0]['name'],
                    })

        self.failUnless(issue.assignee!=None)
        """

    def testChangeProblemType(self):
        """ 
        Tests adding and removing problem types
        """ 
        pass
        ""
