#!/bin/bash

. ./deploy.ini

cd $BASE_DIR;

docker-compose -f containers/docker-compose.yaml down;

docker rmi -f containers_nlp-web:latest containers_nlp-bert:latest;
