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
   
cp "./edu.washington.tracker.plist" "$plist_dir"
# check if copy was successful
if [ ! -f $plist_loc ]; then
    echo "Error: Could not copy to $plist_loc"
    exit 1
fi

# create labtracker dir if necessary
if [[ ! -e "$script_dir" || ! -d "$script_dir" ]]; then
    # echo 'labtracker dir does not exist'
    mkdir "$script_dir"
fi

# copy over tracker.py if directory exists
if [ -e "$script_dir" ]; then
    cp "./tracker.py" "$script_loc"
else # check that directory got created
    echo "Error: Could not make directory $script_dir" 
    exit 1
fi

# check that script got copied
if [ ! -f "$script_loc" ]; then
    echo "Error: Could not copy to $script_loc" 
    exit 1
fi

echo "Successfully installed Labtracker client script"
exit 0
