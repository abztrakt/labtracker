#!/bin/bash

source "tools/functions.sh";

for xx in `getApps`; do  
	python manage.py sqlreset $xx | grep '^DROP' | sed 's/;/ CASCADE;/';
done 
