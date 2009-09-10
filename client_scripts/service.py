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
try:
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

            #self.stop_event = win32event.CreateEvent(None, 0, 0, None)
            self.isAlive = True

        """
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
        """

        def SvcDoRun(self):
            import servicemanager

            # listen for login/logout 
            #servicemanager.RegisterServiceCtrlHandler(self._svc_name_, self.ServiceCtrlHandler)
               
            #self.ReportServiceStatus(win32service.SERVICE_RUNNING)

            try:

                try:
                    urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackerstart.html')
                except Exception, e:
                    pass

                import win32com.client
                import win32com.server.policy
                import pythoncom

                ## from Sens.h
                # XXX don't need all of these, simply lists of the the SENS interfaces
                SENSGUID_PUBLISHER = "{5fee1bd6-5b9b-11d1-8dd2-00aa004abd5e}" 
                SENSGUID_SUBSCRIBER_LCE ="{d3938ab0-5b9d-11d1-8dd2-00aa004abd5e}" 
                SENSGUID_SUBSCRIBER_WININET = "{d3938ab5-5b9d-11d1-8dd2-00aa004abd5e}" 
                SENSGUID_EVENTCLASS_NETWORK = "{d5978620-5b9f-11d1-8dd2-00aa004abd5e}" 
                SENSGUID_EVENTCLASS_LOGON = "{d5978630-5b9f-11d1-8dd2-00aa004abd5e}" 
                SENSGUID_EVENTCLASS_ONNOW = "{d5978640-5b9f-11d1-8dd2-00aa004abd5e}" 
                SENSGUID_EVENTCLASS_LOGON2 = "{d5978650-5b9f-11d1-8dd2-00aa004abd5e}" 

                ## from EventSys.h 
                CLSID_CEventSystem="{4E14FBA2-2E22-11D1-9964-00C04FBBB345}" 
                CLSID_CEventSubscription="{7542e960-79c7-11d1-88f9-0080c7d771bf}" 
                IID_IEventSubscription="{4A6B0E15-2E38-11D1-9965-00C04FBBB345}" 

                PROGID_EventSystem = "EventSystem.EventSystem" 
                PROGID_EventPublisher = "EventSystem.EventPublisher" 
                PROGID_EventClass = "EventSystem.EventClass" 
                PROGID_EventSubscription = "EventSystem.EventSubscription" 
                PROGID_EventPublisherCollection = "EventSystem.EventPublisherCollection" 
                PROGID_EventClassCollection = "EventSystem.EventClassCollection" 
                PROGID_EventSubscriptionCollection = "EventSystem.EventSubscriptionCollection" 
                PROGID_EventSubsystem = "EventSystem.EventSubsystem" 
                EVENTSYSTEM_PUBLISHER_ID = "{d0564c30-9df4-11d1-a281-00c04fca0aa7}" 
                EVENTSYSTEM_SUBSYSTEM_CLSID = "{503c1fd8-b605-11d2-a92d-006008c60e24}" 

                IID_ISensLogon = "{d597bab3-5b9f-11d1-8dd2-00aa004abd5e}" 

                class SensLogon(win32com.server.policy.DesignatedWrapPolicy):
                    _com_interfaces_ = [IID_ISensLogon]
                    _public_methods_ = [
                        'Logon',
                        'Logoff',
                        'StartShell',
                        'DisplayLock',
                        'DisplayUnlock',
                        'StartScreenSaver',
                        'StopScreenSaver'
                        ]

                    def __init__(self):
                        self._wrap_(self)

                    def Logon(self, *args):
                        try:
                            urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackerlogin.html')
                        except Exception, e:
                            pass
                        #print 'Logon'
                        #print args

                    def Logoff(self, *args):
                        try:
                            urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackerlogout.html')
                        except Exception, e:
                            pass

                    def StartShell(self, *args):
                        pass

                    def DisplayLock(self, *args):
                        pass

                    def DisplayUnlock(self, *args):
                        pass

                    def StartScreenSaver(self, *args):
                        pass

                    def StopScreenSaver(self, *args):
                        pass

                sl=SensLogon() 
                subscription_interface=pythoncom.WrapObject(sl) 

                event_system=win32com.client.Dispatch(PROGID_EventSystem) 

                event_subscription=win32com.client.Dispatch(PROGID_EventSubscription) 
                event_subscription.EventClassID=SENSGUID_EVENTCLASS_LOGON 
                event_subscription.PublisherID=SENSGUID_PUBLISHER 
                event_subscription.SubscriptionName='Python subscription' 
                event_subscription.SubscriberInterface=subscription_interface 

                event_system.Store(PROGID_EventSubscription, event_subscription) 
            except:
                import urllib2
                try:
                    urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackererror.html')
                except Exception, e:
                    pass

            #while self.isAlive:
            #    pass


            #    try:
            #        urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackerping.html') 
            #        time.sleep(10)
            #    except:
            #        pass
            #try:
            #    urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackerlogoff.html')
            #except Exception, e:
            #    pass
                

            #win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
                #servicemanager.LogInfoMsg('labtracker - running')
                #urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtracker')
                    #win32api.SleepEx(10000, True)
            #win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

            #servicemanager.LogInfoMsg('labtracker - stopped')

        def SvcStop(self):
            self.isAlive = False
            """
            try:
                import servicemanager
                try:
                    with open('c:\Documents and Settings\Administrator\stop.txt','w') as file:
                        file.write('svc stop ran')
                except:
                    pass
            """
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            """
                try:
                    urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackerlogoff.html')
                except Exception, e:
                    pass
            """
#            win32event.SetEvent(self.stop_event) 
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
            """
                #servicemanager.LogInfoMsg('labtracker - received stop signal')
                #self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                #win32event.SetEvent(self.hWaitStop)
            except:
                pass
            """

    if __name__ == '__main__':
        try:
#            win32api.SetConsoleCtrlHandler(lambda x: True, True)
            HandleCommandLine(Labtracker)
        except:
            pass
except:
    import urllib2
    try:
        urllib2.urlopen('http://inspiredlychee.eplt.washington.edu/labtrackererror.html')
    except Exception, e:
        pass
