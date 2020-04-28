#!/bin/bash

. ./deploy.ini

cd $BASE_DIR;

for INDEX in meta paragraphs
do
  python3 py/create_index.py --index_file="data/json/$INDEX.json" --index_name=$INDEX;
  echo "Index $INDEX created.";
done
