@ECHO off
ECHO Installing LabTracker Client Script...
MD c:\Program Files\LabTracker\ /I
XCOPY dist "c:\Program Files\LabTracker\" 
ECHO Installing Log-On and Log-Off group policies...
regedit /s policies.reg
PAUSE
ECHO ON