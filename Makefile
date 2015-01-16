# Unit-testing, docs, etc.

APPLICATION_DIR=base
VIRTUALENV?=virtualenv

setup_environment: _install_system_dependencies _install_application_dependencies
	rm -fr env
	$(VIRTUALENV) --no-site-packages env

setup_development_environment: setup_environment _install_application_dependencies _install_development_application_dependencies

upgrade_application_dependencies: _rmpyc
	@echo "\n\n>> Upgrading application dependencies \n\n"
	mkdir -p .download_cache
	./scripts/install_application_dependencies.sh production upgrade
	rm -rf .download_cache

upgrade_development_application_dependencies: _rmpyc
	mkdir -p .download_cache
	./scripts/install_application_dependencies.sh development upgrade
	rm -rf .download_cache

run: _clean
	@echo "\nStarting Flask internal server...\n"
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
	PYTHONPATH=`pwd` env/bin/alembic --config base/alembic.ini upgrade head

migrate_test_environment: _clean
	APPLICATION_ENV=test PYTHONPATH=`pwd` env/bin/alembic --config base/alembic.ini upgrade head

_install_system_dependencies:
	@echo "\n\n>> Installing system dependencies \n\n"
	./scripts/install_system_dependencies.sh
	rm -rf .download_cache

_install_application_dependencies: _rmpyc
	@echo "\n\n>> Installing application dependencies \n\n"
	mkdir -p .download_cache
	./scripts/install_application_dependencies.sh production
	rm -rf .download_cache

_install_development_application_dependencies: _rmpyc
	@echo "\n\n>> Installing development application dependencies \n\n"
	mkdir -p .download_cache
	./scripts/install_application_dependencies.sh development
	rm -rf .download_cache

_clean: _rmpyc
	rm -rf .download_cache

_rmpyc:
	find . -name "*.pyc" -exec rm -rf {} \;
