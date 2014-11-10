#!/usr/bin/env bash

UPGRADE=""
if [[ $2 == "upgrade" ]]; then
	UPGRADE="--upgrade"
fi

echo -e "\n## Installing application dependencies..."
env/bin/pip install $UPGRADE --download-cache=.download_cache/ -r requirements

if [[ $1 == "development" ]]; then
	echo -e "\n## Installing development environment dependencies..."
	env/bin/pip install $UPGRADE --download-cache=.download_cache/ -r requirements_dev
fi
echo -e "\n## Done"