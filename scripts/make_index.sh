#!/bin/bash

. ./deploy.ini

cd $BASE_DIR;

FILE=`echo "$1" | cut -d'.' -f1`

pip3 install -r py/requirements.txt;
python3 py/create_index.py --index_file="data/$FILE.json" --index_name=$INDEX_NAME;
echo 'Index created. Loading documents..';
python3 py/create_documents.py --data="data/$FILE.csv" --index_name=$INDEX_NAME;
echo "Index popolated. Loading into elasticsearch..";
python3 py/index_documents.py --data="data/$FILE.index";
echo "Done!"
