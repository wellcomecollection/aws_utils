lint:
	docker run --rm --tty --volume $(ROOT):/src wellcome/tox -e lint

test:
	docker run --rm --tty --volume $(ROOT):/src wellcome/tox -e py36
