# Unit-testing, docs, etc.

APPLICATION_DIR=base
VIRTUALENV?=virtualenv

all: setup_development_environment setup_environment

setup_environment: _install_system_dependencies _create_virtualenvironment _install_application_dependencies _generate_production_configuration_files _bootstrap_database

setup_development_environment: setup_environment _install_development_application_dependencies _generate_development_configuration_files _bootstrap_development_database

upgrade_application_dependencies: _rmpyc _create_download_dir
	./scripts/install_application_dependencies.sh production upgrade

upgrade_development_application_dependencies: _rmpyc _clean _create_download_dir
	./scripts/install_application_dependencies.sh development upgrade

run: _clean
	PYTHONPATH=`pwd` env/bin/python $(APPLICATION_DIR)/run.py runserver

shell: _clean
	PYTHONPATH=`pwd` env/bin/python $(APPLICATION_DIR)/run.py shell

tests:
	PYTHONPATH=`pwd` env/bin/nosetests $(APPLICATION_DIR)

coverage:
	PYTHONPATH=`pwd` env/bin/coverage --ignore-errors -m -r $(APPLICATION_DIR)/*

pep8:
	PYTHONPATH=`pwd` env/bin/pep8 -r $(APPLICATION_DIR)

migrate: _clean
	PYTHONPATH=`pwd` env/bin/alembic --config base/app/configs/alembic.ini upgrade head

migrate_test_environment: _clean
	APPLICATION_ENV=test PYTHONPATH=`pwd` env/bin/alembic --config base/app/configs/alembic.ini upgrade head

_bootstrap_database:
	PYTHONPATH=`pwd` env/bin/python ./scripts/bootstrap_database.py base.app

_bootstrap_development_database:
	APPLICATION_ENV=testing PYTHONPATH=`pwd` env/bin/python ./scripts/bootstrap_database.py base.app

_create_virtualenvironment:
	rm -rf ./env
	$(VIRTUALENV) --no-site-packages env

_install_system_dependencies:
	./scripts/install_system_dependencies.sh
	rm -rf .download_cache

_install_application_dependencies: _rmpyc _create_download_dir
	./scripts/install_application_dependencies.sh production

_install_development_application_dependencies: _rmpyc _create_download_dir
	./scripts/install_application_dependencies.sh development

_create_download_dir:
	rm -rf .download_cache
	mkdir -p .download_cache

_generate_production_configuration_files:
	./scripts/generate_configuration_files.sh $(APPLICATION_DIR) production

_generate_development_configuration_files:
	./scripts/generate_configuration_files.sh $(APPLICATION_DIR) development

_clean: _rmpyc
	rm -rf .download_cache

_rmpyc:
	find . -name "*.pyc" -exec rm -rf {} \;
