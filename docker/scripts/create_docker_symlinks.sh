#!/bin/bash

ln -sf /srv/www/base/configs/application.id /srv/www/base/current/base/app/configs/application.id
ln -sf /srv/www/base/configs/alembic.ini /srv/www/base/current/base/app/configs/alembic.ini
ln -sf /srv/www/base/configs/development.py /srv/www/base/current/base/app/configs/development.py
ln -sf /srv/www/base/configs/testing.py /srv/www/base/current/base/app/configs/testing.py
