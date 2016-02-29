# Makefile to expose main functionalities of this application.
# Dependency on docker

all: _run_container
run: _run_container

test:
	docker run --rm -it \
		--name base_app_test \
		-v `pwd`:/srv/www/base/current \
		fathineos/base_app make -f docker/Makefile test

shell:
	docker run --rm -it \
		--name base_app_shell
		-v `pwd`:/srv/www/base/current \
		fathineos/base_app make -f docker/Makefile shell

container:
	docker build --rm \
		-f docker/Dockerfile \
		-t fathineos/base_app .

push_container:
	docker push fathineos/base_app

_run_container:
	docker run --rm -it \
		--name base_app_run \
		-v `pwd`:/srv/www/base/current \
		-p 6000:6000 fathineos/base_app

_remove_container: stop_container
	docker rm base_app_run

_stop_container:
	docker stop base_app_run
