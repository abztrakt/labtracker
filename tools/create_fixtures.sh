#!/bin/bash

source "tools/functions.sh";

if [[ -z $1 ]]; then
	echo "Must give a prefix"
	exit 1
fi

name=$1
shift

for app in 'auth'; do
    python manage.py dumpdata --format=json --indent=2 ${app} >> "./test/fixtures/${name}.json"
done

for app in `getApps`; do
	[[ -e "${app}/fixtures" ]] || mkdir "${app}/fixtures"
	python manage.py dumpdata --format=json --indent=2 ${app} > "${app}/fixtures/${name}.json"
done

