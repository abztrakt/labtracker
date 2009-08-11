from datetime import datetime
from hashlib import md5

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404

import simplejson

import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils
import Tracker.models as t_models

def getStatus(status):
    """
    From given status, determine which status flags need to be updated
    """
    flags = {
        "drop": [],     # status flags to drop
        "add": []       # status flags to add
    }

    if status == "login":
        flags['add'].append(m_models.Status.objects.get(name="Inuse"))
    elif status == "logout":
        flags['drop'].append(m_models.Status.objects.get(name="Inuse"))

    return flags

def updateMachine(request, name):
    """
    Update a specific machine's status
    Give machine a new status, update it's time, and user
    The request must include a status, and a user
    """

    machine = get_object_or_404(m_models.Item, name=name)

    # make sure that the IP is the same as that in the machine to be updated

    try:
        pass
        if request.META['REMOTE_ADDR'] != machine.ip:
            return HttpResponseForbidden()
    except:
        return HttpResponseForbidden()


    data = request.REQUEST.copy()

    if data.has_key('status') and data.has_key('user'):
        # interpret the status
        flags = getStatus(data.get('status'))

        userhash = md5(data['user'])

        try:
            user = c_models.LabUser.objects.get(pk=userhash.hexdigest())
            user.accesses += 1
        except ObjectDoesNotExist, e:
            user = c_models.LabUser(user_id=userhash.hexdigest())
            user.accesses = 1
        except Exception, e:
            #print "Could not get user %s" % e
            return HttpResponseServerError()

        user.save()
        time = datetime.now()
        #print machine.status.all()

        for st in flags['drop']:
            machine.status.remove(st)

        for st in flags['add']:
            machine.status.add(st)

        #m_utils.updateStatus(machine, status, user, time)
        #print machine.status.all()

        stat_msg = ", ".join([st.name for st in machine.status.all()])

        return HttpResponse("%s - %s - %s -- %s" % (machine, stat_msg, user, time))

    return HttpResponseServerError()

def track(request, action, macs):

    # must be https
#    if not request.is_secure():
#        pass
        #return HttpResponseForbidden()

    data = request.REQUEST.copy() 

    macs_list = macs.split(',')

    for mac in macs_list:
        machine = m_models.Item.objects.filter(mac1=mac)

        if len(machine) == 0:
            machine = m_models.Item.objects.filter(mac2=mac) 

        if len(machine) == 1:
            break 
    
    # make sure we matched a machine
    if len(machine) == 0:
        # could not find machine based on mac
        return HttpResponseServerError()

    machine = machine[0]

    if data.has_key('status') and data.has_key('user'):
         # interpret the status
        flags = getStatus(data.get('status'))

        userhash = md5(data['user'])

        try:
            user = c_models.LabUser.objects.get(pk=userhash.hexdigest())
            user.accesses += 1
        except ObjectDoesNotExist, e:
            user = c_models.LabUser(user_id=userhash.hexdigest())
            user.accesses = 1
        except Exception, e:
            #print "Could not get user %s" % e
            return HttpResponseServerError()

        user.save()
        time = datetime.now()
        #print machine.status.all()

        for st in flags['drop']:
            machine.status.remove(st)

        for st in flags['add']:
            machine.status.add(st)

        #m_utils.updateStatus(machine, status, user, time)
        #print machine.status.all()

        stat_msg = ", ".join([st.name for st in machine.status.all()])

        #return HttpResponse("%s - %s - %s -- %s" % (machine, stat_msg, user, time))
        # TODO we need to do data verification to ensure proper data is submitted
        logout = None
        stats = t_models.Statistics.objects.filter(logout_time__isnull=True, item=machine)
        if stats.count() == 1:
            logout = stats[0]

        if action == 'login':
            # create login
	    # TODO we need to be able to collect netid or regid as well!
            # If previous session is not closed, track logout.
            if logout:
                logout.logout_time = time
                if logout.ping_time:
                    logout.logout_time = logout.ping_time
                logout.save()

            login = t_models.Statistics(login_time=time, item=machine)
            login.save()
            m_models.History()
        elif action == 'logout':
            # create logout for previous login and save
            if logout:
                logout.logout_time = time
                logout.save()
            pass
        elif action == 'ping':
            # create time for ping, which can be used to track improper logouts
            if logout:
                logout.ping_time = time
                logout.save()
            pass
        else:
            # shouldn't match URLs
            return HttpResponseForbidden()
        
        return HttpResponse("%s - %s - %s -- %s" % (machine, stat_msg, user, time))
        #return HttpResponse('success')
    return HttpResponseServerError()
