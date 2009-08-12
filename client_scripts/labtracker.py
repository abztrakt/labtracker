import urllib
import urllib2
import getpass
import sys
import os
from optparse import OptionParser

LABTRACKER_URL = "labtracker.eplt.washington.edu"
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
    # windows systems
    if sys.platform == 'win32':
        for line in os.popen("ipconfig /all"):
            if line.lstrip().startswith('Physical Address'):
                mac = line.split(':')[1].strip().replace('-',':')
                break
        return mac
    # linux/apple systems
    else:
        for line in os.popen("/sbin/ifconfig"):
            if line.find('Ether') > -1:
                mac = line.split()[4]
            break
        return mac 

def get_data(status): 
    # get user info from machine
    user = getpass.getuser()
    data = urllib.urlencode({'user': user, 'status': status})
    return data

def track():
    global ACTIONS, options
    if hasattr(options, "action"):

        # verify that option.action is a valid action
        if options.action in ACTIONS:  
            # TODO ensure that the secure url is accessible
            # TODO ensure that the post data (in variable 'data') can be sent

            # with data argument, request is automatically POST
            try:
                req = urllib2.Request(url="http://%s/tracker/%s/%s/" % (LABTRACKER_URL, 
                                                                options.action, get_mac()),
                                data=get_data(options.action)) # for now, status update is synchronized with actions
                urllib2.urlopen(req)
            except:
                pass
        else:
            print 'Action attribute not valid. Actions are %s.' % get_actions_list()
    else:
        print 'Need action argument: %s' % get_actions_list()
       

if __name__ == '__main__':
    track() 
