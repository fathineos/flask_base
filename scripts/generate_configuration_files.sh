#!/usr/bin/env bash

APPLICATION_DIR=$1
if [ -z "$APPLICATION_DIR" ]; then
    echo "APPLICATION_DIR was not provided, exiting..."
    exit 1
fi
if [[ $2 == "development" ]]; then
    cp -n $APPLICATION_DIR/app/configs/development.py.example $APPLICATION_DIR/app/configs/development.py
    cp -n $APPLICATION_DIR/app/configs/testing.py.example $APPLICATION_DIR/app/configs/testing.py
    exit 0
else
    cp -n $APPLICATION_DIR/app/configs/application.id.example $APPLICATION_DIR/app/configs/application.id
    cp -n $APPLICATION_DIR/app/configs/default.py.example $APPLICATION_DIR/app/configs/default.py
    exit 0
fi
