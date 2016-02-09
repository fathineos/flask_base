#!/bin/bash

if [ -f /.dockerinit ]; then
    echo "base" > .DATABASE_NAME
    echo "mysql_1" > .DATABASE_HOST
    echo "base" > .DATABASE_USER
    echo "base" > .DATABASE_PASS
else
    echo "base" > .DATABASE_NAME
    echo "127.0.0.1" > .DATABASE_HOST
    echo "root" > .DATABASE_USER
    echo "root" > .DATABASE_PASS
fi
