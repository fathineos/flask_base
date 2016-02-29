#!/bin/bash

make -f docker/Makefile _configuration_symlinks &&\
make -f docker/Makefile run
