#!/bin/bash

. ./deploy.ini

cd $BASE_DIR;

DATA="data/raw/meta.pkl"
META="data/index/meta.index"

echo "Refactoring $DATA...";
python3 py/rawMeta.py --pickle="$DATA" --index_name='meta'

echo "Indexing $META...";
N=$(cat $META  | wc -l);
python3 py/indexing.py --data="$META" --size=$N;
