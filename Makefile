ROOT = $(shell git rev-parse --show-toplevel)


$(ROOT)/.docker/tox: $(ROOT)/docker/tox.Dockerfile
	docker build --tag tox --file docker/tox.Dockerfile docker
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/tox

$(ROOT)/.docker/tooling: $(ROOT)/docker/tooling.Dockerfile
	docker build --tag tooling --file docker/tooling.Dockerfile docker
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/tooling


lint: $(ROOT)/.docker/tox
	docker run --rm --tty --volume $(ROOT):/src tox -e lint

test: $(ROOT)/.docker/tox
	docker run --rm --tty --volume $(ROOT):/src tox -e py36

check-release-file: $(ROOT)/.docker/tooling
	docker run --rm --tty \
		--volume $(ROOT):/src \
		tooling scripts/check-release-file.py

deploy: $(ROOT)/.docker/tooling
	env | grep -v TRAVIS_COMMIT_MESSAGE > env.list
	docker run --rm --tty \
		--env-file env.list \
		--volume $(ROOT):/src \
		--volume ~/.ssh:/root/.ssh \
		tooling scripts/deploy.py


.PHONY: lint test check-release-file deploy
