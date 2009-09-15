#!/bin/bash

plist_dir="/Library/LaunchAgents"
plist_loc="${plist_dir}/edu.washington.tracker.plist"

script_dir="/Library/Application Support/Labtracker"
script_loc="${script_dir}/tracker.py"

# make sure user is root
if [[ $EUID -ne 0 ]]; then
    echo 'need to run the script as root'
    exit 1
fi

# delete plist
if [ -f $plist_loc ]; then
    rm "$plist_loc" 
fi

# check if plist deleted
if [ -f $plist_loc ]; then
    echo "Error: Could not remove file $plist_loc"
    exit 1
fi

# remove script
if [ -f "$script_loc" ]; then
    rm "$script_loc"
fi

if [ -f "$script_loc" ]; then
    echo "Error: Could not remove file $script_loc"
    exit 1
fi

# remove script folder
if [ -e "$script_dir" ]; then
    rmdir "$script_dir"
fi

# check that folder was removed
if [ -e "$script_dir" ]; then
    echo "Error: Could not remove directory $script_dir"
    exit 1
fi

echo "Successfully uninstalled Labtracker client script"
exit 0
