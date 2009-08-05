import urllib
import urllib2
import getpass

LABTRACKER_URL = "labtracker.eplt.washington.edu"

ACTIONS = ('login','logout','ping')

# on startup hit url
# url structure

#Get user info from machine
user = getpass.getuser()
data = urllib.urlencode({'user': user})

try:
    urllib2.openurl("https://%s/%s/%s" % (LABTRACKER_URL, ACTIONS[0], get_mac()), data)
except:
    pass

def get_mac():
    # works on windows only
    for line in os.popen("ipconfig /all"):
        if line.lstrip().startswith('Physical Address'):
            mac = line.split(':')[1].strip().replace('-',':')
            break
    return mac
