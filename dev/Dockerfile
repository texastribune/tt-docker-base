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
ENV PIP_NO_BINARY=psycopg2
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
  && poetry config virtualenvs.create false --local \
  && poetry install --no-dev
ENV NPM_CONFIG_LOGLEVEL warn
ENV NPM_CONFIG_PREFIX=/node_modules
ENV PATH=$PATH:/node_modules/.bin
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE False
ENV PIP_NO_BINARY=psycopg2

# Install ligbnetls30, needed workaround for this issue to install nodesource:  https://github.com/nodesource/distributions/issues/1266
RUN apt update && \
    apt install libgnutls30

# Install nodejs from nodesource
RUN \
  echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
  echo "deb https://deb.nodesource.com/node_14.x stretch main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  apt-get -qq update && \
  apt-get -qq install nodejs > /dev/null && \
  rm -rf /var/lib/apt/lists/*

COPY install-tools.sh /
RUN /install-tools.sh

WORKDIR /

RUN poetry install

COPY node /node
WORKDIR /node
RUN npm install
RUN cp -r node_modules /
WORKDIR /