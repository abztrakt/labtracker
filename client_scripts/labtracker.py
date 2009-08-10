import urllib
import urllib2
import getpass
import sys
import os

LABTRACKER_URL = "labtracker.eplt.washington.edu"
ACTIONS = ('login','logout','ping')

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

# get user info from machine
user = getpass.getuser()
data = urllib.urlencode({'user': user})

# TODO ensure that the secure url is accessible
# TODO ensure that the post data (in variable 'data') can be sent

# with data argument, request is automatically POST
try:
    urllib2.Request(url="http://%s/tracker/%s/%s" % (LABTRACKER_URL, 
                                                    ACTIONS[0], get_mac()),
                    data=data)
except:
    pass

