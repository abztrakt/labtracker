"""
install.py -- installation script for Labtracker client scripts
author: Taylor McKay
"""

import _winreg
import shutil

PROG_NAME = "labtracker.py"
PROG_PATH = "C:\\Program Files\\Labtracker\\"
REG_SUB_KEY = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

"""
exp = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        )
"""

# put startup program into place 
shutil.copy(PROG_NAME,PROG_PATH)

"""
# creates a sub folder within the registry named labtracker
# need to set value as labtracker
_winreg.SetValue(
                    _winreg.HKEY_LOCAL_MACHINE,
                    "Software\\Microsoft\\Windows\\CurrentVersion\\Run\\Labtracker",
                    _winreg.REG_SZ,
                    "c:\\python26\\python.exe"
                )
"""

# open the key
key = _winreg.OpenKey(
#                        _winreg.HKEY_LOCAL_MACHINE,
                        _winreg.HKEY_CURRENT_USER,
                        REG_SUB_KEY,
                        0,
                        _winreg.KEY_WRITE
                    )

# add Labtracker program to startup
_winreg.SetValueEx(
            key, 
            "Labtracker",
            0,
            _winreg.REG_SZ,
            PROG_PATH + PROG_NAME,
        )

"""
Catch this signal to see shutdown
WM_QUERYENDSESSION

WM_ENDSESSION

Make the window not visible
WS_VISIBLE
"""
