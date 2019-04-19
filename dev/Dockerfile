FROM texastribune/base:0.1.12-base

ENV NPM_CONFIG_LOGLEVEL warn
ENV NODE_VERSION 8.11.3
ENV NPM_CONFIG_PREFIX=/node_modules
ENV PATH=$PATH:/node_modules/.bin

RUN \
  echo "deb https://deb.nodesource.com/node_8.x stretch main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
  wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  apt-get update && \
  apt-get install -yqq nodejs yarn && \
  npm i -g npm@^6 && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /

RUN poetry install

COPY package.json yarn.lock /
RUN yarn && rm package.json yarn.lock

ONBUILD WORKDIR /app
ONBUILD COPY scripts /app/scripts
ONBUILD RUN ./scripts/install-tools.sh

ONBUILD COPY .babelrc.js /app/
ONBUILD COPY webpack /app/webpack
ONBUILD COPY config /app/config
ONBUILD COPY scripts /app/scripts
ONBUILD COPY www /app/www
ONBUILD COPY package.json /app/
