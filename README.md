[![Build Status](https://travis-ci.org/fathineos/flask_base.svg?branch=master)](https://travis-ci.org/fathineos/flask_base)

# Flask-Base library #

Flask Base is a library based on Flask and provides commonly used functionality to web applications which run on top of it. It may also run as a stand alone application.
[Flask](http://flask.pocoo.org/) is a microframework for Python to easily create Web Apps.

Dependencies: Docker

### What is this repository for? ###

* Handling application Configurations
* Modular Database Connection initialization and migration mechanism with alembic
* Testing Framework with nose, coverage, pep8
* Libraries for common API functionalities


### Setup environment ###

```
make all
```

### Running Application ###
##### Run as app container with flask web server (for development) #####
```
make run
```

##### Run unittests: #####
```
make test
```

##### Run python shell #####
```
make shell
```

Check [Makefile](https://github.com/fathineos/flask_base/blob/master/Makefile) for available commands
