#!/bin/bash

DATE=""
VER=""

curl https://storage.googleapis.com/golang/go1.9.linux-amd64.tar.gz | tar -zxf - -C /usr/local
PATH=$PATH:/usr/local/go/bin:
export PATH
curl -L https://github.com/gravitational/teleport/releases/download/v2.3.0-rc2/teleport-v2.3.0-rc2-linux-amd64-bin.tar.gz | tar -zxf - -C ~/ && cd /root/teleport/ && make install
source ~/.bash_profile
