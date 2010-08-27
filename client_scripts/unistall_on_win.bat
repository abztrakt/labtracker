@ECHO off
ECHO Uninstalling LabTracker Client...
RD /s /q "C:\Program Files\LabTracker"
ECHO Removing Group Policies...
REGEDIT /s uninstall.reg
ECHO Complete
PAUSE