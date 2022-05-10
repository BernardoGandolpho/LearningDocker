FROM python:3.8-alpine
WORKDIR /usr/src/poke_api

ENV MONGODB_URL="mongodb+srv://root-poke-api:7f6904c51f8d51e0a26e7bc36fda27bd@pokemonapi.juwxl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

COPY ./requirements.txt /usr/src/poke_api/requirements.txt

RUN set -eux \
&& apk add --no-cache --virtual .build-deps build-base \
libressl-dev libffi-dev gcc musl-dev python3-dev \
&& pip install --upgrade pip setuptools wheel \
&& pip install -r /usr/src/poke_api/requirements.txt \
&& rm -rf /root/.cache/pip

EXPOSE 5000
COPY . /usr/src/poke_api
CMD ["python", "main.py"]
