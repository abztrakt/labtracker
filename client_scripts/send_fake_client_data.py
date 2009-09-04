#!/usr/bin/env python

from optparse import OptionParser 
import time
import sys
import os

# so we can use the labtracker's models
os.chdir('../')
sys.path.append(os.getcwd())
import settings
from django.core.management import setup_environ 
setup_environ(settings)

from Machine.utils import get_all_macs
from tracker import ACTIONS, _track

MAX_PINGS = 10 # number of pings per machine update NOT IMPLEMETED
MACS = get_all_macs()
MACS_LEN = len(MACS)
KEEP_PINGING = True
PAUSE_BETWEEN_PINGS = 1 # seconds between pings

parser = OptionParser()
parser.add_option("-a", "--address", dest="address", 
                help="Address of labtracker ping script") 

parser.add_option("-p", "--ping", action="store_true", dest="ping", 
                help="Send ping signals too") 

(options, args) = parser.parse_args()

if options.address is None:
    options.address = settings.SITE_ADDR 

def ping():
    import random
    import time

    # check address
    import urllib2
    if not options.address.startswith('http://'):
        urllib2.urlopen('http://'+options.address)

    while KEEP_PINGING:
        mac_idx = random.randint(0, MACS_LEN-1)

        print 'creating history for machine address %s' % MACS[mac_idx]

        # login
        _track(options.address, ACTIONS[0], MACS[mac_idx], data=ACTIONS[0])

        # ping
        if options.ping:
            for idx in range(0, random.randint(1, MAX_PINGS)):
                _track(options.address, ACTIONS[2], MACS[mac_idx], data=ACTIONS[2])
                time.sleep(PAUSE_BETWEEN_PINGS)
        else:
            time.sleep(1)

        # logoff
        _track(options.address, ACTIONS[1], MACS[mac_idx], data=ACTIONS[1])

    sys.exit(0)

try:
    print '' 
    print 'LABTRACKER: Send fake client data' 
    print 'Press Ctrl+c to exit'
    print '' 
    print 'Beginning data transmission...'

    ping()

except KeyboardInterrupt, e:
    KEEP_PINGING = False
    print 'Exiting...'
