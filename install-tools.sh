#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail
#set -o xtrace

echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
apt-get -qq update
apt-get -qq install vim less > /dev/null
cd /tmp
wget -q https://github.com/monochromegane/the_platinum_searcher/releases/download/v2.2.0/pt_linux_amd64.tar.gz
tar -xf pt_linux_amd64.tar.gz
cp pt_linux_amd64/pt /usr/local/bin
chmod +x /usr/local/bin/pt
echo "set -o vi" >> /etc/bash.bashrc
