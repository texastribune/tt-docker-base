FROM python:3.7-stretch

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
ENV PIP_NO_BINARY=psycopg2
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
  && poetry config settings.virtualenvs.create false \
  && poetry install --no-dev
ENV NPM_CONFIG_LOGLEVEL warn
ENV NODE_VERSION 12.13.0
ENV NPM_CONFIG_PREFIX=/node_modules
ENV PATH=$PATH:/node_modules/.bin
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE False
ENV PIP_NO_BINARY=psycopg2

RUN \
  echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
  echo "deb https://deb.nodesource.com/node_12.x stretch main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
  wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  apt-get -qq update && \
  apt-get -qq install nodejs yarn > /dev/null && \
  npm i -g npm@^6 && \
  rm -rf /var/lib/apt/lists/*

COPY install-tools.sh /
RUN /install-tools.sh

WORKDIR /

RUN poetry install

COPY package.json yarn.lock /
RUN yarn
