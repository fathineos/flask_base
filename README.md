[![Build Status](https://travis-ci.org/fathineos/flask_base.svg?branch=master)](https://travis-ci.org/fathineos/flask_base)

# Flask-Base library #

Flask Base is a library based on Flask and provides commonly used functionality to web applications which run on top of it. It may also run as a stand alone application.
[Flask](http://flask.pocoo.org/) is a microframework for Python to easily create Web Apps.

### What is this repository for? ###

* Handling application Configurations
* Modular Database Connection initialization and migration mechanism with alembic
* Testing Framework with nose, coverage, pep8
* Libraries for common functionalities


### Installation ###

1.Install system dependencies
```
sudo apt-get install python-virtualenv, python-pip, mysql, python-mysql
```
2.Setup environment:
```
make all
```

### Run as standalone app ###
```
make run
```

Read Makefile for available commands
