FROM python:3-alpine

RUN apk update && apk add git

RUN pip install requests

WORKDIR /src
VOLUME ["/src"]

ENTRYPOINT ["python"]
