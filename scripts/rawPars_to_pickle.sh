#!/bin/bash

. ./deploy.ini

cd $BASE_DIR;

DATA='data/raw/paragraphs/'
C=0

for f in `ls $DATA*.pkl | sort -V`
do
  echo "Processing $f...";
  python3 py/rawPars.py --pickle=$f --counter=$C;
  let C+=1
done
