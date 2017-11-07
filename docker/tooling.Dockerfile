FROM python:3-alpine

RUN apk update && apk add git openssl openssl-client

RUN pip install requests twine

WORKDIR /src
VOLUME ["/src"]

ENTRYPOINT ["python"]
