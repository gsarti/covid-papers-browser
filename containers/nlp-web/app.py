import os
import random
import sys
from pprint import pprint
import spacy
import json
import argparse
from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
from bert_serving.client import BertClient
from nltk.tokenize import sent_tokenize
from flask_cors import CORS
from support import elastic_query, query_filters, as_dict, get_search_results, get_relevant_span, get_paper, get_paragraphs_similarity, get_vector,  get_vector_numpy
from flask import session


SEARCH_SIZE = 10
INDEX_NAME = os.environ['INDEX_NAME']
DEBUG = False

app = Flask(__name__)
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['TESTING'] = False

CORS(app)

nlp = spacy.load("en_core_web_sm")


@app.route("/")

@app.route("/authors", methods=['GET'])
def authors():
    with open('authors.json', 'r') as f:
    	authors = json.load(f)
    return jsonify(authors)

@app.route("/years", methods=['GET'])
def years():
    client = Elasticsearch('nlp-elasticsearch:9200')
    response = client.search(
        index="meta",
        body={"size":0,
             "aggs": {
              "Terms_Aggregation" : {
                  "terms": {"field": "publish_time.keyword"}
               }
           }
        }
    )
    dates  = []
    for d in response['aggregations']['Terms_Aggregation']['buckets']:
        dates.append(list(d.values()))
    years = {}
    for d in dates:
        y = d[0][:4]
        c = int(d[1])
        if y not in years.keys():
            years[y] = c
        else:
            years[y] += c
    YYYY = []
    for k,v in years.items():
        YYYY.append([k,v])
    return jsonify(YYYY)

@app.route("/licenses", methods=['GET'])
def license():
    client = Elasticsearch('nlp-elasticsearch:9200')

    response = client.search(
        index="meta",
        body={"size":0,
             "aggs": {
              "Terms_Aggregation" : {
                  "terms": {"field": "license"}
               }
           }
        }
    )
    licenses = []
    for d in response['aggregations']['Terms_Aggregation']['buckets']:
        licenses.append(list(d.values()))
    return jsonify(licenses)


@app.route("/journals", methods=['GET'])
def journal():
    client = Elasticsearch('nlp-elasticsearch:9200')

    response = client.search(
        index="meta",
        body={"size":0,
             "aggs": {
              "Terms_Aggregation" : {
                  "terms": {"field": "journal"}
               }
           }
        }
    )
    journals = []
    for d in response['aggregations']['Terms_Aggregation']['buckets']:
        journals.append(list(d.values()))
    return jsonify(journals)


@app.route('/status')
def status():
    bc = BertClient(ip='nlp-bert')
    return jsonify(bc.server_status)


@app.route('/paper', methods=['GET','POST'])
def search():
    try:
        query = request.get_json().get('query')
    except AttributeError:
        query = ''


    publish_time = request.get_json().get('year')
    if publish_time == [] or publish_time == '':
        years = None
    else:
        years = '-'.join(str(v[0]) for v in publish_time)
    authors = request.get_json().get('author')
    journal = request.get_json().get('journal')
    license = request.get_json().get('license')
    page = request.get_json().get('page')
    if page is None:
        page=1

    session['query'] = query

    if query != '':
        query_vector = get_vector(query)
        embeddings = 'title_abstract_embeddings'
        filters = query_filters(license, years, journal, authors)
        script_query = elastic_query(filters, embeddings, query_vector)
        results, total = get_search_results(page, SEARCH_SIZE, script_query)
        results = { 'data': results, 'total' : total}
        return jsonify(results)
    else:
         return {}

@app.route('/singlearticle', methods=['GET','POST'])
def get_singlepage():
    query = session['query']

    try:
        cord_id_s = ""
        cord_id = request.get_json().get('cord_id')
        if cord_id is None:
             cord_id_s= ""
        else:
             cord_id_s = str(cord_id)
        print(cord_id_s, file=sys.stderr)
    except AttributeError:
        cord_id_s = ''

    paper = get_paper(cord_id_s)
    query_vector = get_vector(query)
    paragraphs = get_paragraphs_similarity(cord_id_s, query_vector)
    doc = nlp(query)
    pars = []
    scores = []
    for i in range(len(paragraphs)):
        par = paragraphs[i]
        scores.append(par['_score'])
        pars.append(((i, (par['_source']['par_title'], par['_source']['paragraph']))))
    indices = get_relevant_span([t.text for t in doc if not t.is_stop], [p[1] for _, p in pars])
    singlepage = as_dict(paper,pars,scores,indices)
    return jsonify(singlepage)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

