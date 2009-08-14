"""
labtracker service

Usage:
    c:\Python26\python.exe service.py install
    c:\Python26\python.exe service.py start 

To remove:
    run 'cmd' as admin    
    sc stop labtracker
    sc delete labtracker
"""

import win32service
#import win32serviceutil
from win32serviceutil import ServiceFramework, HandleCommandLine
import win32api

class Labtracker(ServiceFramework):
    _svc_name_ = "labtracker"
    _svc_display_name_ = "labtracker - LST lab stats tool"

    def __init__(self, args):
        ServiceFramework.__init__(self, args)
        self.isAlive = True

    def SvcDoRun(self):
        import servicemanager

        while self.isAlive:
           # do some pinging 
           servicemanager.LogInfoMsg('labtracker - running')
           win32api.SleepEx(10000, True)

        servicemanager.LogInfoMsg('labtracker - stopped')

    def SvcStop(self):
        import servicemanager
        
        servicemanager.LogInfoMsg('labtracker - received stop signal')

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

        self.isAlive = False

# for running the service even when 
# logout occurs
def ctrlHandler(ctrlType):
    return True

if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)
    HandleCommandLine(Labtracker)
