#!/bin/bash

dir="/Library/Application Support/Labtracker"

login_hook_file="mac_login_hook.sh"
login_hook_loc="${dir}/${login_hook_file}"

logout_hook_file="mac_logout_hook.sh"
logout_hook_loc="${dir}/${logout_hook_file}"

script_file="tracker.py"
script_loc="${dir}/${script_file}"


# make sure user is root
if [[ $EUID -ne 0 ]]; then
    echo 'need to run the script as root'
    exit 1
fi

# remove tracker.py 
if [ -f "$script_loc" ]; then
    rm "$script_loc"
fi

# remove login hook 
if [ -f "$login_hook_loc" ]; then
    rm "$login_hook_loc"
fi

# remove logout hook 
if [ -f "$logout_hook_loc" ]; then
    rm "$logout_hook_loc"
fi

# make sure we remove the files
if [[ -f "$script_loc" || -f "$login_hook_loc" || -f "$logout_hook_loc" ]]; then
    echo "Error: Could not remove some files" 
    exit 1
fi

# remove script folder
if [ -e "$dir" ]; then
    rmdir "$dir"
fi

# check that folder was removed
if [ -e "$dir" ]; then
    echo "Error: Could not remove directory $dir"
    exit 1
fi

# remove hook configurations
`defaults delete com.apple.loginwindow LoginHook`
`defaults delete com.apple.loginwindow LogoutHook`

echo "Successfully uninstalled Labtracker client script"
exit 0
