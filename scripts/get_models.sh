#!/bin/bash

. ./deploy.ini

cd $BASE_DIR;

pip3 install --upgrade pip

pip3 install -r py/get_models_requirements.txt;

python3 py/get_models.py --model $1
