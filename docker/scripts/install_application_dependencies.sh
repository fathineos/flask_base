#!/bin/bash

UPGRADE=""
if [[ $2 == "upgrade" ]]; then
    UPGRADE="--upgrade"
fi

${ENV}/bin/pip install $UPGRADE -r requirements

if [[ $1 == "development" ]]; then
    ${ENV}/bin/pip install $UPGRADE -r requirements_dev
fi
