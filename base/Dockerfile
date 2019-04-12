FROM python:3.6-stretch

WORKDIR /app

RUN apt-get update -qq && \
  DEBIAN_FRONTEND=noninteractive apt-get -yq install \
  software-properties-common \
  apt-transport-https \
  apt-utils \
  libjpeg-dev \
  libxml2-dev \
  libxslt1-dev \
  libproj-dev \
  libpq-dev \
  gdal-bin \
  libffi-dev \
  libmemcached-dev

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry==0.12.12 \
  && poetry config settings.virtualenvs.create false \
  && poetry install --no-dev
