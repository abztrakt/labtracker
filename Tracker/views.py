from datetime import datetime
from hashlib import md5
from decimal import *
import time as t


from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt #There is no possible way a client machine could get a valid csrf_token
def track(request, action, macs):

    # must be https
    #if not request.is_secure():
        # WTF is this pass doing here, ericwu?
        #pass
        #return HttpResponseForbidden()

    data = request.REQUEST.copy() 

    macs_list = macs.split(',')
    for mac in macs_list:
	mac = mac.replace('-',':')
	mac_temp = mac.replace(':','-')
	machine = m_models.Item.objects.filter(Q(mac1__iexact=mac)|Q(mac1__iexact=mac_temp))

        if len(machine) == 0:
            machine = m_models.Item.objects.filter(Q(mac2__iexact=mac)|Q(mac2__iexact=mac_temp)) 

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
        except ObjectDoesNotExist, e:
            user = c_models.LabUser(user_id=userhash.hexdigest())
            user.accesses = 0
        except Exception, e:
            #print "Could not get user %s" % e
            return HttpResponseServerError()

        time = datetime.now()
        #print machine.status.all()

        for st in flags['drop']:
            machine.status.remove(st)

        for st in flags['add']:
            machine.status.add(st)

	#To get last_modified update
	machine.save()
	
        #m_utils.updateStatus(machine, status, user, time)
        #print machine.status.all()

        stat_msg = ", ".join([st.name for st in machine.status.all()])

        #return HttpResponse("%s - %s - %s -- %s" % (machine, stat_msg, user, time))
        # TODO we need to do data verification to ensure proper data is submitted

        stats = m_models.History.objects.filter(machine=machine, session_time__isnull=True)

        # Test if machine has logged out
        logout = None
        if stats.count() == 1:
            logout = stats[0]

        if action == 'login':
        # create login
        # If previous session is not closed, track logout.
            if logout:
                logout.session_time = (t.mktime(time.timetuple()) - t.mktime(logout.login_time.timetuple())) / 60 # Measured in minutes
                logout.session_time = Decimal("%.2f" % logout.session_time)
                logout.save()

	        #the user has logged in to a machine one more time
            user.accesses += 1
            user.save()

            login = m_models.History(login_time=time, machine=machine, user=user)
            login.save()
        elif action == 'logout':
            # create logout for previous login and save
            if logout:
                logout.session_time = (t.mktime(time.timetuple()) - t.mktime(logout.login_time.timetuple())) / 60
                logout.session_time = Decimal("%.2f" % logout.session_time)
                logout.save()
        elif action == 'ping':
            # update the latest session time for the given machine
            try:
                logout = m_models.History.objects.filter(machine=machine, session_time__isnull=False).order_by('-session_time')[0]
            except Exception, e:
                if stats.count() == 1:
                    logout = stats[0]
                else:
                    pass
            logout.session_time = (t.mktime(time.timetuple()) - t.mktime(logout.login_time.timetuple())) / 60
            logout.session_time = Decimal("%.2f" % logout.session_time)
            logout.save()
        else:
            # shouldn't match URLs
            return HttpResponseForbidden()
        
        return HttpResponse("%s - %s - %s -- %s" % (machine, stat_msg, user, time))
        #return HttpResponse('success')
    return HttpResponseServerError()
