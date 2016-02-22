# Makefile to support Docker container setup

APP_DIR = base
ENV ?= $(ENV)

all: _install_system_dependencies _create_virtualenvironment\
	_install_application_dependencies \
	_install_development_application_dependencies \
	_create_config_folder \
	_generate_docker_production_configuration_files \
	_generate_docker_development_configuration_files

upgrade_application_dependencies:
	./docker/scripts/install_application_dependencies.sh production upgrade

upgrade_development_application_dependencies:
	./docker/scripts/install_application_dependencies.sh development upgrade

run: _clean
	PYTHONPATH=`pwd` $(ENV)/bin/python $(APP_DIR)/run.py runserver -h 0.0.0.0 -p 6000

# migrate: _clean
# 	PYTHONPATH=`pwd` $(ENV)/bin/alembic \
# 		--config base/app/configs/alembic.ini upgrade head

shell: _clean
	PYTHONPATH=`pwd` $(ENV)/bin/python $(APP_DIR)/run.py shell

test: _clean _configuration_symlinks _pep8
	PYTHONPATH=`pwd` $(ENV)/bin/nosetests $(APP_DIR)

test_coverage:
	PYTHONPATH=`pwd` $(ENV)/bin/nosetests --with-coverage \
		--cover-erase --cover-package=$(APP_DIR)

_pep8:
	PYTHONPATH=`pwd` $(ENV)/bin/pep8 --exclude='test_*' -r $(APP_DIR)

_create_virtualenvironment:
	rm -rf $(ENV)
	virtualenv --no-site-packages $(ENV)

_install_system_dependencies:
	apt-get install -qq -y --force-yes  python-virtualenv python-pip \
		libmysqlclient-dev python-dev

_install_application_dependencies:
	./scripts/install_application_dependencies.sh production

_set_database_credentials:
	./docker/scripts/set_database_credentials.sh

_install_development_application_dependencies:
	./scripts/install_application_dependencies.sh development

_create_config_folder:
	mkdir -p /srv/www/base/configs/

_generate_production_configuration_files: _set_database_credentials
	./scripts/generate_configuration_files.sh production \
	$(APP_DIR)/app/configs

_generate_development_configuration_files: _set_database_credentials
	./scripts/generate_configuration_files.sh development \
	$(APP_DIR)/app/configs

_generate_docker_production_configuration_files: _set_database_credentials
	/srv/www/base/frozen/scripts/generate_configuration_files.sh \
		production /srv/www/base/frozen/base/app/configs \
		/srv/www/base/configs

_generate_docker_development_configuration_files: _set_database_credentials
	/srv/www/base/frozen/scripts/generate_configuration_files.sh \
		development /srv/www/base/frozen/base/app/configs \
		/srv/www/base/configs

_configuration_symlinks:
	./docker/scripts/create_docker_symlinks.sh

_clean:
	find . -name "*.pyc" -exec rm -rf {} \;
