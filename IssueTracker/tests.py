import re
from datetime import datetime

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, check_password

import simplejson

from LabtrackerCore import Email
from LabtrackerCore.models import Item, InventoryType, Group 
import LabtrackerCore.models as coreModels
import Machine.models as mModels
import IssueTracker
from IssueTracker import models as iModels

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
        self.failUnlessEqual(302, response.status_code)

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

        self.failUnlessEqual(200, response.status_code)

        # convert the response content to a python dict
        data = simplejson.JSONDecoder().decode(response.content)

        ret_groups = set([data[key]["name"] for key in data.keys()])
        self.assertTrue(len(ret_groups) > 0)
        self.assertEquals(0, len(groups.difference(ret_groups)))

    def testAjaxItems(self):
        """
        Grab the items for Machine groups 'Empty Group' and 'Group1', ensure 
        they return correct items
        """
        self.client.login(username=self.user.username, password=self.password)

        # fetch the two groups
        group_1 = mModels.Group.objects.filter(name='Group1').all()[0]
        group_e = mModels.Group.objects.filter(name='Empty Group').all()[0]

        url = reverse('IssueTracker.views.ajax.getItems')

        def fetchJSON(group):
            response = self.client.post(url,
                { 'type': 'json', 'group_id': group.pk })

            self.failUnlessEqual(response.status_code, 200)

            # convert the response content to a python dict
            return simplejson.JSONDecoder().decode(response.content)


        # fetch for empty group first
        data = fetchJSON(group_e)
        items = data['items']
        self.failUnlessEqual(0, len(items))

        # now do the group1
        data = fetchJSON(group_1)
        data_items = data['items']
        self.assertTrue(len(data_items) > 0)

        # make sure that the items returned by json are the same as those in DB
        items = set([item.pk for item in group_1.core.items.all()])
        ret_items = set([data_items[key]["item_id"] for key in data_items.keys()])

        self.assertEquals(0, len(items.difference(ret_items)))

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
                'problem_type': [iModels.ProblemType.objects.all()[0].pk,],
                'status':       ['3'],
                'group':	3, #abritrary group pk that exists
		'item':		3, #arbitrary item pk that exists
                'description':  "All the machines in the lab are broken."
            })

        self.failUnlessEqual(num_issues + 1, iModels.Issue.objects.all().count())

        issue = iModels.Issue.objects.filter(title=title).reverse()[0]
        self.issue = issue

        # make sure that the issue was created
        self.assertTrue(last_pk < issue.pk)

        self.failUnlessEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('IssueTracker-view', args=[self.issue.pk,]),
                status_code=302, target_status_code=200)

        # now make sure that we can actually view that issue
        response = self.client.get(reverse('IssueTracker-view', args=[self.issue.pk]))

        self.assertTemplateUsed(response, "view.html")

    def testCreateIssueEmail(self):
        """
        Create an issue for an item that is part of a group with a primary contact
        """

        self.client.login(username=self.user.username, password=self.password)

        issues = iModels.Issue.objects.all()
        num_issues = issues.count()

        # get a group with a primary contact
        group = mModels.Group.objects.filter(contact__user__username='zhaoz', name='CRC').all()[0]

        # ensure that group has at least one item
        item = mModels.Item.objects.all()[0]
        group.items.add(item)

        response = self.client.post(reverse('createIssue'), {
                'title':        "Issue for %s" % (item.pk),
                'it':           item.it_id,
                'item':         item.pk,
                'problem_type': [iModels.ProblemType.objects.all()[0].pk,],
                'status':       ['3'],
		'group':	3, #arbitrary group pk that exists
		'item':		3, #arbitrary item pk that exists
                'description':  "Test problem"
            })
        self.failUnlessEqual(num_issues + 1, iModels.Issue.objects.all().count())

        # primary contact should get an email here
        self.assertEqual(1, len(mail.outbox))

class IssueSearchTest(TestCase):
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
        
        self.client.login(username=self.user.username, password=self.password)
        title = "Unique Issue XAZZER"
        self.issue = iModels.Issue(it = coreModels.InventoryType.objects.all()[0],
                    title = title,
                    reporter = self.user,
                    description= "All the machines in the lab are broken.",
		    group = mModels.Group.objects.get(pk=3), #arbitrary known group and item primary keys
		    item = mModels.Item.objects.get(pk=3))
        self.issue.save()

    def testSearchID(self):
        """
        Search with given id, see if it brings up the issue
        """
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(reverse('issueSearch'), {
                'search_term':  self.issue.pk
            })

        self.assertRedirects(response, reverse('IssueTracker-view', args=[self.issue.pk]))

    def testQuickSearch(self):
        """
        Test a simple search
        """
        self.client.login(username=self.user.username, password=self.password)

        issues = IssueTracker.search.titleSearch("XAZZER")
        self.assertEquals(len(issues), 1)

        response = self.client.get(reverse('issueSearch'), {
                'search_term':  "XAZZER"
            })
        self.assertTemplateUsed(response, "issue_list.html")

        # test and make sure that the response has only one issue
        issue_link_re = re.compile(r'<a href="/issue/\d+/">')

        self.assertEquals(1, len(issue_link_re.findall(response.content)))

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
        self.email.addTo('testemail_person@example.com')
        self.email.send()

        self.assertEqual(1, len(mail.outbox))


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

        self.issue = iModels.Issue.objects.\
                filter(group__group__contact__isnull=False).all()[0]

        self.client.login(username='testuser', password=self.password)

    def tearDown(self):
        self.user.delete()

    def testAddComment(self):
        """
        Tests adding comment
        """
        self.client.post(reverse('IssueTracker-view', args=[1]),
                        {   'issue': self.issue.pk,
                            'user': self.user, 
                            'comment': 'here is a test comment'
                        })

        comment = iModels.IssueComment.objects.get(issue=self.issue)
        self.failUnless(comment is not None)

        self.assertEqual(1, len(mail.outbox))
        self.failUnlessEqual(None, self.issue.resolve_time)

    def testAddCC(self):
        """
        adding/removing CC list
        """

        self.issue = iModels.Issue.objects.\
                filter(group__group__contact__isnull=False,cc__isnull=False).all()[0]

        # starting count
        num_cc = self.issue.cc.count()

        # attempt to add the testUser to the testIssue
        self.client.post(reverse('IssueTracker-modIssue', args=[self.issue.pk]),
                            {'action': 'addcc',
                            'user': self.user.username})
        self.issue = iModels.Issue.objects.get(pk=self.issue.pk)
        self.failUnlessEqual(num_cc+1, self.issue.cc.count())
        self.failUnlessEqual(1, self.issue.cc.filter(username=self.user.username).count())
        self.failUnlessEqual(None, self.issue.resolve_time)

        # test removal

        self.client.post(reverse('IssueTracker-modIssue', args=[self.issue.pk]),
                            {'action': 'dropcc',
                            'user': self.user.pk})
        self.failUnlessEqual(num_cc, self.issue.cc.count())
        self.failUnlessEqual(0, self.issue.cc.filter(username=self.user.pk).count())
        self.failUnlessEqual(None, self.issue.resolve_time)

    def testChangeAssignee(self):
        """
        Tests changing the assignee of an issue
        """

        # test getting an issue with no assignee, and changing it
        issue = iModels.Issue.objects.filter(assignee__isnull=True)[0]
        self.client.post(reverse('IssueTracker-view', args=[issue.pk]), {
                        'assignee'          : self.user.pk,
                    })

        issue = iModels.Issue.objects.get(pk=issue.pk)
        self.failUnlessEqual(self.user, issue.assignee)
        self.failUnlessEqual(None, issue.resolve_time)

        # test getting an issue with an assignee, and changing it
        issue = iModels.Issue.objects.filter(assignee__isnull=False)[0]
        self.client.post(reverse('IssueTracker-view', args=[issue.pk]), {
                        'assignee'          : self.user.pk,
                    })

        issue = iModels.Issue.objects.get(pk=issue.pk)
        self.failUnlessEqual(self.user, issue.assignee)

        # make sure that the resolved time has not changed
        self.failUnlessEqual(None, issue.resolve_time)

    def testChangeProblemType(self):
        """ 
        Tests adding and removing problem types
        """ 
        # get some problem types
        all_ptypes = iModels.ProblemType.objects.all()

        def withPtypeSet(ptypes):
            #new_ptype = ptypes[0]
            response = self.client.post(
                reverse('IssueTracker-view', args=[self.issue.pk]), {
                            'problem_type'          : [ptype.pk for ptype in ptypes],
                        })

            self.failUnlessEqual(302, response.status_code)

            self.issue = iModels.Issue.objects.get(pk=self.issue.pk)

            # make sure that it only has one ptype, and is the one we assigned
            self.failUnlessEqual(len(ptypes), self.issue.problem_type.count())

            ptype_set = set(ptypes)
            cur_ptypes = set(self.issue.problem_type.all())
            self.failUnlessEqual(0, len(ptype_set.difference(cur_ptypes)))

        withPtypeSet([all_ptypes[0]])   # test with ptypes[0]
        withPtypeSet(all_ptypes[0:3])   # change the ptypes, involves adding
        withPtypeSet(all_ptypes[2:3])   # change the ptypes, involves removing

    def testResolveIssue(self):
        """
        test resolving an issue
        """
        issue = iModels.Issue.objects.filter(resolved_state__isnull=True)[0] #removed ,item__isnull=True

        resolution = iModels.ResolveState.objects.all()[0]
        curTime = datetime.now()

        self.client.post(reverse('IssueTracker-view', args=[issue.pk]), 
                         { 'resolved_state': resolution.pk, })

        issue = iModels.Issue.objects.get(pk=issue.pk)
        self.failUnlessEqual(resolution, issue.resolved_state)

        self.failIfEqual(None, issue.resolve_time)

        self.failUnless(issue.resolve_time >= curTime)


