#!/bin/sh

docker-compose down
docker-compose build
clear
docker-compose up $1