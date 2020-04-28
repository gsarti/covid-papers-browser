#!/bin/bash

. ./deploy.ini

cd ../models;

#biobert-base v1.1. pubmed 1M
wget https://github.com/naver/biobert-pretrained/releases/download/v1.1-pubmed/biobert_v1.1_pubmed.tar.gz;

tar -xvf biobert_v1.1_pubmed.tar.gz;

cd biobert_v1.1_pubmed;

rename "s/\-1000000//" model*;

for model in $(ls model*); do mv $model bert_$model ; done

rm ../biobert_v1.1_pubmed.tar.gz;
