#!/bin/bash

find ./ -mindepth 2 -regextype posix-extended -type f -iregex '.*\.py$' | xargs wc -l
