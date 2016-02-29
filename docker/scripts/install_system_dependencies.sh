#!/bin/bash

if [[ $(uname) == "Linux" ]]; then
    # This will download a installation script and run it
    curl -sSL https://get.docker.com/ | sudo sh

    # Also add your user to the docker group so you don't need to use sudo for docker commands
    sudo gpasswd -a ${USER} docker;
    sudo service docker restart
elif [[ $(uname) == "Darwin" ]]; then
    # Not implemented for OSX yet
fi
exit 0
