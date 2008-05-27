from datetime import datetime
from md5 import md5

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404

import simplejson

import LabtrackerCore.models as c_models
import Machine.models as m_models
import Machine.utils as m_utils

def updateMachine(request, name):
    """
    Update a specific machine's status
    Give machine a new status, update it's time, and user
    The request must include a status, and a user
    """
    machine = get_object_or_404(m_models.Item, item__name=name)

    data = request.POST.copy()

    if data.has_key('status') and data.has_key('user'):
        status = get_object_or_404(m_models.Status, pk=data['status'])
        userhash = md5(data['user'])

        try:
            user = c_models.LabUser.objects.get(pk=userhash.hexdigest())
            user.accesses += 1
        except ObjectDoesNotExist, e:
            user = c_models.LabUser(user_id=userhash.hexdigest())
            user.accesses = 1
        except Exception, e:
            return HttpResponseServerError()

        user.save()
        time = datetime.now()
        m_utils.updateStatus(machine, status, user, time)

        return HttpResponse("%s - %s - %s -- %s" % (machine, status, user, time))

    return HttpResponseServerError()

