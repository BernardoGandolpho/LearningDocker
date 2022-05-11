FROM python:3.8-alpine
WORKDIR /usr/src/poke_api

COPY ./requirements.txt /usr/src/poke_api/requirements.txt

RUN set -eux \
&& apk add --no-cache --virtual .build-deps build-base \
libressl-dev libffi-dev gcc musl-dev python3-dev \
&& pip install --upgrade pip setuptools wheel \
&& pip install -r /usr/src/poke_api/requirements.txt \
&& rm -rf /root/.cache/pip

EXPOSE 8008
COPY . /usr/src/poke_api
CMD ["python", "main.py"]
