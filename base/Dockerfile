FROM python:3.6-stretch

WORKDIR /

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update -qq && \
  apt-get -qq install \
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
  libmemcached-dev > /dev/null

COPY pyproject.toml poetry.lock /
RUN pip --quiet install poetry==0.12.12 \
  && poetry config settings.virtualenvs.create false \
  && poetry --quiet install --no-dev
