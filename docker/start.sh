#!/usr/bin/env bash

set -e

export DOCKER_HOST=$(ip route show | grep 'default via' | awk '{print $3}')
export PYTHONPATH=/home/user/code

# mkdir -p /home/user/code/smwebsite/media
# chown user /home/user/code/smwebsite/media
# chmod 700 /home/user/code/smwebsite/media

exec $@
