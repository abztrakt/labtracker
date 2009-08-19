"""
labtracker service

To install:
    run 'cmd' as admin    

Usage:
    c:\Python26\python.exe service.py install
    c:\Python26\python.exe service.py start 
    c:\Python26\python.exe service.py remove

Also:
    sc stop labtracker
    sc delete labtracker
"""

import win32service
#import win32serviceutil
from win32serviceutil import ServiceFramework, HandleCommandLine
import win32api
import win32event

import urllib
import urllib2
import time

class Labtracker(ServiceFramework):
    _svc_name_ = "Labtracker"
    _svc_display_name_ = "Labtracker"

    def __init__(self, args):
        ServiceFramework.__init__(self, args)

        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True

    def ServiceCtrlHandler(self, status):
        # login
        if status == win32service.WIN32_SERVICE_CONTROL_SESSIONCHANGE:
            try:
                urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackerlogin.html')
            except Exception, e:
                pass

        # shutdown
        elif status == win32service.WIN32_SERVICE_CONTROL_PRESHUTDOWN:
            try:
                urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackerlogout.html')
            except Exception, e:
                pass

    def SvcDoRun(self):
        import servicemanager

        # listen for login/logout 
        servicemanager.RegisterServiceCtrlHandler(self._svc_name_, self.ServiceCtrlHandler)
           
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

        while self.isAlive:
            try:
                urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackerping.html') 
                time.sleep(10)
            except:
                pass

        #win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            #servicemanager.LogInfoMsg('labtracker - running')
            #urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtracker')
                #win32api.SleepEx(10000, True)
        #win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

        #servicemanager.LogInfoMsg('labtracker - stopped')

    def SvcStop(self):
        import servicemanager
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.isAlive = False
        try:
            urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackerlogoff.html')
        except Exception, e:
            pass
        win32event.SetEvent(self.stop_event) 
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        #servicemanager.LogInfoMsg('labtracker - received stop signal')
        #self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        #win32event.SetEvent(self.hWaitStop)

if __name__ == '__main__':
    #win32api.SetConsoleCtrlHandler(lambda x: True, True)
    HandleCommandLine(Labtracker)
