"""
install.py -- installation script for Labtracker client scripts
author: Taylor McKay
"""

import _winreg
import shutil

PROG_NAME = "labtracker.py"
PROG_PATH = "C:\\Program Files\\Labtracker\\"

"""
exp = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        )
"""

# put startup program into place 
shutil.copy(PROG_NAME,PROG_PATH)

# add Labtracker program to startup
_winreg.SetValueEx(
            _winreg.HKEY_LOCAL_MACHINE,
            "Labtracker",
            0,
            _winreg.REG_SZ,
            PROG_LOC,
        )


