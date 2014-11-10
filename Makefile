# Unit-testing, docs, etc.

PROJECT_DIR=flask_base
APPLICATION_DIR=base
VIRTUALENV?=virtualenv

setup_environment: install_system_dependencies install_application_dependencies
	rm -fr env
	$(VIRTUALENV) --no-site-packages env
	@echo "\n\n>> Run 'source env/bin/activate'"

setup_development_environment: setup_environment install_application_dependencies install_development_application_dependencies

run: clean
	@echo "\nStarting Flask internal server...\n"
	PYTHONPATH=`pwd` env/bin/python $(APPLICATION_DIR)/run.py runserver

shell: clean
	PYTHONPATH=`pwd` env/bin/python $(APPLICATION_DIR)/run.py shell

clean: rmpyc
	rm -rf .download_cache

rmpyc:
	find . -name "*.pyc" -exec rm -rf {} \;
	@echo "done"

install_system_dependencies:
	./scripts/install_system_dependencies.sh
	rm -rf .download_cache

install_application_dependencies: rmpyc
	mkdir -p .download_cache
	./scripts/install_application_dependencies.sh production
	rm -rf .download_cache

install_development_application_dependencies: rmpyc
	mkdir -p .download_cache
	./scripts/install_application_dependencies.sh development
	rm -rf .download_cache

upgrade_application_dependencies: rmpyc
	mkdir -p .download_cache
	./scripts/install_application_dependencies.sh production upgrade
	rm -rf .download_cache

upgrade_development_application_dependencies: rmpyc
	mkdir -p .download_cache
	./scripts/install_application_dependencies.sh development upgrade
	rm -rf .download_cache

coverage:
	PYTHONPATH=`pwd` env/bin/coverage --ignore-errors -m -r $(APPLICATION_DIR)/*

pep8:
	PYTHONPATH=`pwd` env/bin/pep8 -r $(APPLICATION_DIR)
