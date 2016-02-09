APP_DIR = base
ENV ?= env

all: setup_development_environment setup_production_environment

setup_production_environment: _install_system_dependencies \
	_create_virtualenvironment \
	_install_application_dependencies \
	_generate_production_configuration_files

setup_development_environment: setup_production_environment \
	_install_development_application_dependencies \
	_generate_development_configuration_files

upgrade_application_dependencies:
	./scripts/install_application_dependencies.sh production upgrade

upgrade_development_application_dependencies:
	./scripts/install_application_dependencies.sh development upgrade

run: _clean
	PYTHONPATH=`pwd` $(ENV)/bin/python $(APP_DIR)/run.py runserver

shell: _clean
	PYTHONPATH=`pwd` $(ENV)/bin/python $(APP_DIR)/run.py shell

test: _clean pep8
	PYTHONPATH=`pwd` $(ENV)/bin/nosetests $(APP_DIR)

test_coverage:
	PYTHONPATH=`pwd` $(ENV)/bin/nosetests --with-coverage \
		--cover-erase --cover-package=$(APP_DIR)

pep8:
	PYTHONPATH=`pwd` $(ENV)/bin/pep8 --exclude='test_*' -r $(APP_DIR)

migrate: _clean
	PYTHONPATH=`pwd` $(ENV)/bin/alembic \
		--config base/app/configs/alembic.ini upgrade head

migrate_test_environment: _clean
	APPLICATION_ENV=test PYTHONPATH=`pwd` $(ENV)/bin/alembic \
		--config base/app/configs/alembic.ini upgrade head

_create_virtualenvironment:
	rm -rf $(ENV)
	virtualenv --no-site-packages $(ENV)

_install_system_dependencies:
	./scripts/install_system_dependencies.sh

_install_application_dependencies:
	./scripts/install_application_dependencies.sh production

_set_database_credentials:
	. scripts/set_database_credentials.sh

_install_development_application_dependencies:
	./scripts/install_application_dependencies.sh development

_generate_production_configuration_files: _set_database_credentials
	./scripts/generate_configuration_files.sh production \
	$(APP_DIR)/app/configs

_generate_development_configuration_files: _set_database_credentials
	./scripts/generate_configuration_files.sh development \
	$(APP_DIR)/app/configs

_clean:
	find . -name "*.pyc" -exec rm -rf {} \;
