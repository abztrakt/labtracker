#!/bin/bash

# goes through all files and greps out XXX, TODO, and FIXME

find ./ -regextype posix-extended -type f -iregex ".*\.(html|py)$" | xargs egrep 'TODO|FIXME|XXX' -A 3 -B 2 --color=auto -n
