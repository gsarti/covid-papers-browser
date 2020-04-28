#!/bin/bash

cd $BASE_DIR;
. ./deploy.ini

SIZE=$(cat data/meta.index | wc -l)

python3 py/indexing.py --data="data/meta.index" --size=$SIZE;
 
