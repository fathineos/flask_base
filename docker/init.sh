#!/bin/bash

make -f docker/Makefile _docker_configuration_symlinks &&\
make -f docker/Makefile run
