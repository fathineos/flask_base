#!/bin/bash

if [[ $(uname) == "Linux" ]]; then
    if command -v apt-get >/dev/null; then
        install_cmd="apt-get install -qq -y --force-yes"
    fi
    if command -v sudo >/dev/null; then
        sudo="sudo"
    fi
    $sudo $install_cmd python-virtualenv \
        python-pip \
        libmysqlclient-dev \
        python-dev
elif [[ $(uname) == "Darwin" ]]; then
    if ! command -v "brew" >/dev/null 2>&1 ; then
        ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    fi
    brew install python
    sudo pip install virtualenv
fi
exit 0
