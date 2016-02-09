#!/bin/bash

ENV=$1
if [ -z $ENV ]; then
    echo "ENV was not provided, exiting..."
    exit 1
fi
SOURCE_DIR=$2
if [ -z $SOURCE_DIR ]; then
    echo "SOURCE_DIR was not provided, exiting..."
    exit 1
fi
TARGET_DIR=$3
if [ -z $TARGET_DIR ]; then
    TARGET_DIR=$SOURCE_DIR
fi

DATABASE_NAME=`cat .DATABASE_NAME`
DATABASE_HOST=`cat .DATABASE_HOST`
DATABASE_USER=`cat .DATABASE_USER`
DATABASE_PASS=`cat .DATABASE_PASS`
if [[ $(uname) == "Linux" ]]; then
    cmd="sed -i.bak"
elif [[ $(uname) == "Darwin" ]]; then
    cmd="sed -i .bak"
fi

cp $SOURCE_DIR/alembic.ini.example $TARGET_DIR/alembic.ini
$cmd "s/#DATABASE_NAME#/${DATABASE_NAME}/g" $TARGET_DIR/alembic.ini
$cmd "s/#DATABASE_USER#/${DATABASE_USER}/g" $TARGET_DIR/alembic.ini
$cmd "s/#DATABASE_PASS#/${DATABASE_PASS}/g" $TARGET_DIR/alembic.ini
$cmd "s/#DATABASE_HOST#/${DATABASE_HOST}/g" $TARGET_DIR/alembic.ini

if [[ $ENV == "development" ]]; then
    cp $SOURCE_DIR/development.py.example $TARGET_DIR/development.py
    $cmd "s/#DATABASE_NAME#/${DATABASE_NAME}/g" $TARGET_DIR/development.py
    $cmd "s/#DATABASE_USER#/${DATABASE_USER}/g" $TARGET_DIR/development.py
    $cmd "s/#DATABASE_PASS#/${DATABASE_PASS}/g" $TARGET_DIR/development.py
    $cmd "s/#DATABASE_HOST#/${DATABASE_HOST}/g" $TARGET_DIR/development.py
    cp $SOURCE_DIR/testing.py.example $TARGET_DIR/testing.py
fi

rm $TARGET_DIR/*.bak
echo $ENV > $SOURCE_DIR/application.id
