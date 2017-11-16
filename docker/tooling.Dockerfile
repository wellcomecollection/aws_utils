FROM python:3-alpine

RUN apk update && apk add openssl openssh-client
RUN apk add --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/main/ git

RUN pip install requests twine

WORKDIR /src
VOLUME ["/src"]

ENTRYPOINT ["python"]
