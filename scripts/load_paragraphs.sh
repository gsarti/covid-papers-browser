#!/bin/bash

. ./deploy.ini

cd $BASE_DIR;

for f in `ls data/index/paragraphs/*.index | sort -V`
do
  echo "Indexing $f file...";
  N=$(cat $f | wc -l)
  python3 py/indexing.py --data="$f" --size=$N;
done
echo "Done!"
