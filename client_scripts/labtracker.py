import urllib2


LABTRACKER_URL = "labtracker.eplt.washington.edu"

ACTIONS = ('login','logout','ping')

# on startup hit url
# url structure

try:
    urllib2.openurl("https://%s/%s/%s" % (LABTRACKER_URL, ACTIONS[0], get_mac()))
except:
    pass

def get_mac():
    # works on windows only
    for line in os.popen("ipconfig /all"):
        if line.lstrip().startswith('Physical Address'):
            mac = line.split(':')[1].strip().replace('-',':')
            break
    return mac
