#!/usr/bin/env python

import urllib
#import urllib2
import getpass
import sys
import os
from optparse import OptionParser

DEBUG = False
NO_SSL = False # This should really only be set to True for testing.

LABTRACKER_URL = "labtracker.eplt.washington.edu"
if DEBUG:
    LABTRACKER_URL = "walnut.eplt.washington.edu:8000"
    import httplib
    httplib.HTTPConnection.debuglevel = 1
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
    if sys.platform == 'win32':
        for line in os.popen("ipconfig /all"):
            if line.lstrip().startswith('Physical Address'):
                possible_mac = line.split(':')[1].strip().replace('-',':')
            # On machines with multiple active interfaces, we want to send the MAC associated with the IPv4 Address
            elif line.lstrip().startswith('IPv4 Address'):
                mac = possible_mac
        return mac
    # os x 
    elif sys.platform == 'darwin':
        for line in os.popen("/sbin/ifconfig"):
            if line.lower().find('ether') > -1:
                mac = line.split()[1]
            	break
        return mac
    elif sys.platform == 'linux2':
        for line in os.popen("/sbin/ifconfig"):
            if line.lower().find('hwaddr') > -1:
                mac = line.split()[-1]
                break
        return mac

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
        urllib.urlopen("http://%s/tracker/%s/%s/" % (url,action,mac),get_data(action))

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
        else:
            print 'Action attribute not valid. Actions are %s.' % get_actions_list()
    else:
        print 'Need action argument: %s' % get_actions_list()

if __name__ == '__main__':
    track() 
