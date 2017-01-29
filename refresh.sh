#!/usr/bin/env bash

docker-compose stop
docker-compose kill
docker-compose build
docker-compose up