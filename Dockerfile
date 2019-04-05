FROM python:3.6-stretch

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
#ENV LANGUAGE en_US.UTF-8

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV NPM_CONFIG_LOGLEVEL warn
ENV NODE_VERSION 8.11.3

RUN \
  apt-get update && \
  apt-get install -yqq apt-transport-https
RUN \
  echo "deb https://deb.nodesource.com/node_8.x stretch main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
  wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  apt-get update && \
  apt-get install -yqq nodejs yarn && \
  npm i -g npm@^6 && \
  rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip==19.0.3

#COPY requirements.txt /app/requirements.txt
#RUN pip install -r /app/requirements.txt
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
WORKDIR /app
RUN poetry config settings.virtualenvs.create false && \
  poetry install --no-dev
#
# Front-end
#
#WORKDIR /app
#COPY package.json yarn.lock /app/
#RUN yarn
