from datetime import datetime
from hashlib import md5

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404

import simplejson

import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils

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

