# Makefile to expose main functionalities of this application.
# Dependency on docker

all: run

run:
	docker run -v `pwd`:/srv/www/base/current -p 6000:6000 --name base_app \
		fathineos/base_app

stop:
	docker stop base_app

test:
	docker run -it -v `pwd`:/srv/www/base/current fathineos/base_app \
		make -f docker/Makefile test

shell:
	docker run -it -v `pwd`:/srv/www/base/current fathineos/base_app \
		make -f docker/Makefile shell

container:
	docker build --rm -f docker/Dockerfile -t fathineos/base_app .

push_container:
	docker push fathineos/base_app

upgrade_application_dependencies:
	docker run -it -v `pwd`:/srv/www/base/current fathineos/base_app \
		make -f docker/Makefile upgrade_application_dependencies

upgrade_development_application_dependencies:
	docker run -it -v `pwd`:/srv/www/base/current fathineos/base_app \
		make -f docker/Makefile upgrade_development_application_dependencies
