FROM texastribune/base

ENV NPM_CONFIG_LOGLEVEL warn
ENV NODE_VERSION 8.11.3

RUN \
  echo "deb https://deb.nodesource.com/node_8.x stretch main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
  wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  apt-get update && \
  apt-get install -yqq nodejs yarn && \
  npm i -g npm@^6 && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN poetry install

COPY package.json yarn.lock /app/
RUN yarn
