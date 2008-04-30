
function getApps() {
	find ./ -mindepth 2 -maxdepth 2 -iname '__init__.py' | awk -F "/" '{ print $2; }'
}

