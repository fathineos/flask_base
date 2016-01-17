#!/bin/bash

UPGRADE=""
if [[ $2 == "upgrade" ]]; then
    UPGRADE="--upgrade"
fi

# if in docker environment a /.dockerinit exists
if [ ! -f /.dockerinit ]; then
   ENV=env
fi
${ENV}/bin/pip install $UPGRADE -r requirements

if [[ $1 == "development" ]]; then
    env/bin/pip install $UPGRADE -r requirements_dev
fi
