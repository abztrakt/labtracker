#! /usr/bin/env python

""" lab_simulator.py - A script for simulating logins/logouts in a labtracker lab for testing purposes.
"""

from client_scripts import tracker

import settings
from django.core.management import setup_environ

setup_environ(settings)

from labtracker.Machine.models import Item, Status

import datetime
import random
import time

tracker.DEBUG = True
tracker.NO_SSL = True
LABTRACKER_URL = 'walnut.eplt.washington.edu:8000'

inuse = Status.objects.get(name='Inuse')

def sim_login_or_logout(item):
    if not item.unusable:
        try:
            item.status.get(name='Inuse')
            item.status.remove(inuse)
            print "Logging out %s" % item
            tracker._track(LABTRACKER_URL, 'logout', item.mac1)
        except:
            item.status.add(inuse)
            print "Logging in %s" % item
            tracker._track(LABTRACKER_URL, 'login', item.mac1)
    else:
        print "%s is unusable" % item

def main():
    items = Item.objects.all()

    while 1:
        item = Item.objects.get(item_id=random.randrange(1,items.count()))
        sim_login_or_logout(item)
        delay = random.randrange(1,(5460/items.count()))
        time.sleep(delay)

if __name__ == "__main__":
    main()
