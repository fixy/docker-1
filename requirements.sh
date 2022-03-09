#!/bin/sh
yum install -y python3-devel

pip3 install pyyaml psutil

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
