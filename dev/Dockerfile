FROM texastribune/base:0.1.16-base

ENV NPM_CONFIG_LOGLEVEL warn
ENV NODE_VERSION 8.11.3
ENV NPM_CONFIG_PREFIX=/node_modules
ENV PATH=$PATH:/node_modules/.bin
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE False

RUN \
  echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
  echo "deb https://deb.nodesource.com/node_8.x stretch main" > /etc/apt/sources.list.d/nodesource.list && \
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
RUN yarn && rm yarn.lock

ONBUILD WORKDIR /app
ONBUILD COPY scripts /app/scripts
ONBUILD COPY babelrc.js /app/.babelrc.js
ONBUILD COPY config /app/config
ONBUILD COPY package.json /app/
ONBUILD COPY webpack /app/webpack
ONBUILD COPY snollygoster /app/snollygoster
