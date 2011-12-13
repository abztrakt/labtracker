#!/usr/bin/env python

# These values shouldn't be changed here, but you can override them by putting them in a config.py in the same directory.
DEBUG = False
NO_SSL = False # This should really only be set to True for testing.
LABTRACKER_URL = "labtracker.eplt.washington.edu"
OLD_LABTRACKER_URL = "labgeeks.eplt.washington.edu"
LAB = None

import urllib
try:
    import urllib2
except ImportError:
    pass
import getpass
import sys
import os
from optparse import OptionParser
try:
    import config
except:
    pass
try:
    if config.DEBUG:
        DEBUG = config.DEBUG
        import httplib
        httplib.HTTPConnection.debuglevel = 1
except:
    pass
try:
    if config.NO_SSL:
        NO_SSL = config.NO_SSL
except:
    pass
try:
    if config.LABTRACKER_URL:
        LABTRACKER_URL = config.LABTRACKER_URL
except:
    pass
try:
    if config.OLD_LABTRACKER_URL:
        OLD_LABTRACKER_URL = config.OLD_LABTRACKER_URL
except:
    pass
try:
    if config.LAB:
        LAB = config.LAB
except:
    pass

if DEBUG:
    print """
    NO_SSL: %s
    LABTRACKER_URL: %s
    OLD_LABTRACKER_URL: %s
    LAB: %s
    """ % (NO_SSL, LABTRACKER_URL, OLD_LABTRACKER_URL, LAB)

ACTIONS = ('login','logout','ping')

# functions at the module level must be defined
# before being called ;) 
def get_actions_list():
    global ACTIONS
    return ', '.join(ACTIONS)

parser = OptionParser()
parser.add_option("-a", "--action", dest="action", 
                help="Action of script: %s" % get_actions_list()) 

(options, args) = parser.parse_args()

def get_mac():
    # windows 
    mac_addresses = ''
    if sys.platform == 'win32':
        for line in os.popen("ipconfig /all"):
            if line.lstrip().startswith('Physical Address'):
                mac = line.split(':')[1].strip().replace('-',':')
                if mac_addresses=='':
                    mac_addresses=mac
                else:
                    mac_addresses=mac_addresses+','+mac
        return mac_addresses
    # os x 
    elif sys.platform == 'darwin':
        for line in os.popen("/sbin/ifconfig"):
            if line.lower().find('ether') > -1:
                mac = line.split()[1]
                if mac_addresses=='':
                    mac_addresses=mac
                else:
                    mac_addresses=mac_addresses+','+mac
        return mac_addresses
    elif sys.platform == 'linux2':
        for line in os.popen("/sbin/ifconfig"):
            if line.lower().find('hwaddr') > -1:
                mac = line.split()[-1]
                if mac_addresses=='':
                    mac_addresses=mac
                else:
                    mac_addresses=mac_addresses+','+mac
        return mac_addresses

def get_data(status): 
    # get user info from machine
    user = getpass.getuser()
    data = urllib.urlencode({'user': user, 'status': status})
    return data

def _track(url, action, mac, data=None):
    """Lower level track function, useful for testing"""
    try:
    	import urllib2
        secure = ''
        if not NO_SSL:
            secure = 's'
        req = urllib2.Request(url="http%s://%s/tracker/%s/%s/" % (secure, url, action, mac),
                                data=get_data(action)) 
        urllib2.urlopen(req)
    except ImportError:
        if not NO_SSL:
            secure = 's'
        urllib.urlopen("http%s://%s/tracker/%s/%s/" % (secure,url,action,mac),get_data(action))

def _track_old(old_url, lab, action):
    # Get the hostname and split it on ., then only take the first part in case it returns a fqdn
    import socket
    compname = socket.gethostname().split('.')[0]
    compuser = getpass.getuser()

    # Translate actions for new labtracker into states for old labtracker
    state = None
    if action == 'login':
        state = 'closed'
    elif action == 'logout':
        state = 'login'
    else:
        pass

    # Only send data if there's a meaningful state ('ping' doesn't translate to old LT)
    if state:
        #print "https://%s/LabTracker/?op=register&lab=%s&cname=%s&state=%s&user=%s" % (old_url, lab, compname, state, compuser)
        urllib.urlopen( "https://%s/LabTracker/?op=register&lab=%s&cname=%s&state=%s&user=%s" % (old_url, lab, compname, state, compuser))

def track():
    global ACTIONS, options
    if hasattr(options, "action"):

        # verify that option.action is a valid action
        if options.action in ACTIONS:  
            # TODO ensure that the secure url is accessible
            # TODO ensure that the post data (in variable 'data') can be sent

            # with data argument, request is automatically POST
            _track(LABTRACKER_URL,
                    options.action,
                    get_mac(), 
                    options.action)

            if LAB:
                _track_old(OLD_LABTRACKER_URL,
                    LAB,
                    options.action)
        else:
            print 'Action attribute not valid. Actions are %s.' % get_actions_list()
    else:
        print 'Need action argument: %s' % get_actions_list()

if __name__ == '__main__':
    track() 
