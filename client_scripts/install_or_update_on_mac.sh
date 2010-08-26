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
   
# create labtracker dir if necessary
if [[ ! -e "$dir" || ! -d "$dir" ]]; then
    # echo 'labtracker dir does not exist'
    mkdir "$dir"
fi

# copy over tracker.py and hooks if directory exists
if [ -e "$dir" ]; then
    cp "./$script_file" "$script_loc"
    cp "./$login_hook_file" "$login_hook_loc" 
    cp "./$logout_hook_file" "$logout_hook_loc" 
else # check that directory got created
    echo "Error: Could not make directory $dir" 
    exit 1
fi

# check that script got copied
if [[ ! -f "$script_loc" || ! -f "$login_hook_loc" || ! -f "$logout_hook_loc" ]]; then
    echo "Error: Could not copy to $dir" 
    exit 1
fi

# make the scripts executable
chmod 700 "$script_loc"
chmod 700 "$login_hook_loc"
chmod 700 "$logout_hook_loc"

# configure the login/logout hooks

if [[ ! -e "$ihookdir" || ! -d "$ihookdir" ]]; then # if not using iHook, register the hook scripts
	`defaults write com.apple.loginwindow LoginHook "$login_hook_loc"` 
	`defaults write com.apple.loginwindow LogoutHook "$logout_hook_loc"` 
fi

echo "Successfully installed Labtracker client scripts"
exit 0
