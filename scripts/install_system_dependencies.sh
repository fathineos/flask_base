#!/usr/bin/env bash

if [[ $(uname) == "Linux" ]]; then
	# TODO either  make generic for all linuxes or remove
	sudo apt-get install python-virtualenv python-pip libmysqlclient-dev
fi