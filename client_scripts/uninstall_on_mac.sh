#!/bin/bash

dir="/Library/Application Support/Labtracker"
ihookdir="/etc/hooks"

login_hook_file="LI03mac_login_hook.sh"
if [[ -e "$ihookdir" || -d "$ihookdir" ]]; then # if ihookdir exists, use it
	login_hook_loc="${ihookdir}/${login_hook_file}"
else # else treat this like it will be the only LoginHook
	login_hook_loc="${dir}/${login_hook_file}"
fi

logout_hook_file="LO98mac_logout_hook.sh"
if [[ -e "$ihookdir" || -d "$ihookdir" ]]; then # if ihookdir exists, use it
	logout_hook_loc="${ihookdir}/${logout_hook_file}"
else # else treat this like it will be the only LogoutHook
	logout_hook_loc="${dir}/${logout_hook_file}"
fi

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
if [[ ! -e "$ihookdir" || ! -d "$ihookdir" ]]; then # if not using iHook, unregister the hook scripts
	`defaults delete com.apple.loginwindow LoginHook`
	`defaults delete com.apple.loginwindow LogoutHook`
fi

echo "Successfully uninstalled Labtracker client script"
exit 0
