#!/usr/bin/env bash

UPGRADE=""
if [[ $2 == "upgrade" ]]; then
	UPGRADE="--upgrade"
fi

env/bin/pip install $UPGRADE --download-cache=.download_cache/ -r requirements

if [[ $1 == "development" ]]; then
	env/bin/pip install $UPGRADE --download-cache=.download_cache/ -r requirements_dev
fi
