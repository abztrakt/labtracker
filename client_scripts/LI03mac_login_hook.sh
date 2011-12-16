#!/bin/sh

script_loc="/Library/Application Support/Labtracker/tracker.py"

# check that script exists
if [ -f "$script_loc" ]; then
    `"${script_loc}" -u $1 -a login`    
else
    `logger "Labtracker: Could not find script at $script_loc"`
fi
