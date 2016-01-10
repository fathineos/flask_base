#!/bin/bash

if [[ $(uname) == "Linux" ]]; then
    if [ ${DOCKER} ]; then
        apt-get install -qq -y --force-yes python-virtualenv python-pip libmysqlclient-dev python-dev
    else
        sudo apt-get install -qq -y --force-yes python-virtualenv python-pip libmysqlclient-dev python-dev
    fi
elif [[ $(uname) == "Darwin" ]]; then
    if ! command -v "brew" >/dev/null 2>&1 ; then
        ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    fi
    brew install python
    sudo pip install virtualenv
fi
exit 0
