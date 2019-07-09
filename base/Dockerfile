FROM python:3.7.4-stretch

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

ENV PATH=/root/.poetry/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
COPY pyproject.toml poetry.lock /
ENV POETRY_VERSION=0.12.14
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
  && poetry config settings.virtualenvs.create false \
  && poetry install --no-dev
