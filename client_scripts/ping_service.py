#
# A ping service to be 'compiled' into an exe-file with py2exe.
# To install this service, run 'LabtrackerPingService.py install' at command prompt
# 'Then LabtrackerPingService.py start'
#    
#    



#Need to download pywin32 in order to import these module
import win32serviceutil
import win32service
import win32event
import win32evtlogutil
import win32api
import win32con
import time
import sys,os
import urllib2
import urllib
import getpass
import servicemanager


DEBUG = True

LABTRACKER_URL = "labtracker.eplt.washington.edu"
if DEBUG:
    LABTRACKER_URL = "web16.eplt.washington.edu:8000"


def get_mac():
    # windows 
    if sys.platform == 'win32':
        for line in os.popen("ipconfig /all"):
            if line.lstrip().startswith('Physical Address'):
                mac = line.split(':')[1].strip().replace('-',':')
                break
    return mac

def get_data(status): 
    # get user info from machine
	user = getpass.getuser()
	data = urllib.urlencode({'user': user, 'status': status})
	return data


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "LabtrackerService"
    _svc_display_name_ = "Labtracker Service"
    _svc_deps_ = ["EventLog"]
    
	
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.isAlive = True
        

    def SvcStop(self):
        servicemanager.LogInfoMsg("ping service - Stopping")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.isAlive = False
		


    def SvcDoRun(self):
        servicemanager.LogInfoMsg("ping service - Start")
        mac = get_mac()
        while self.isAlive:
            servicemanager.LogInfoMsg("ping service - Ping")
            req= urllib2.Request(url="http://%s/tracker/ping/%s/" %(LABTRACKER_URL,mac),data=get_data('ping')) 
            urllib2.urlopen(req)
            win32api.SleepEx(10000,True)
        servicemanager.LogInfoMsg("ping service - Stopped")
   
def ctrlHandler(ctrlType):
    return True


if __name__ == '__main__':
    # Note that this code will not be run in the 'frozen' exe-file!!!
    win32api.SetConsoleCtrlHandler(ctrlHandler,True)
    win32serviceutil.HandleCommandLine(MyService)
