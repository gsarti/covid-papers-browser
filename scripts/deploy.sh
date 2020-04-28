#!/bin/bash

. ./deploy.ini

cd $BASE_DIR;

docker-compose -f containers/docker-compose.yaml up;
