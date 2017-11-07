ROOT = $(shell git rev-parse --show-toplevel)


$(ROOT)/.docker/flake8: $(ROOT)/docker/flake8.Dockerfile
	docker build --tag flake8 --file docker/flake8.Dockerfile docker
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/flake8


lint: $(ROOT)/.docker/flake8
	docker run --rm --tty --volume $(ROOT):/src flake8
