FROM python:3-alpine

RUN pip install tox

RUN apk update && apk add build-base libffi-dev openssl-dev

WORKDIR /src
VOLUME ["/src"]

ENTRYPOINT ["tox"]
