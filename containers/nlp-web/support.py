import spacy
import argparse
from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
from bert_serving.client import BertClient
from nltk.tokenize import sent_tokenize

def elastic_query(filters, embeddings, query_vector):
    script_query = {
        "script_score": { "query": filters['query'],
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['title_abstract_embeddings']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }
    return script_query

def match(field, content):
    query = {'match': { field: content }}
    return query

def keyword_match(field, keywords):
    query = { 'bool': { 'should' : [match(field,k[0]) for k in keywords] } }
    return query

def query_filters(license, publish_time, journal, authors):
    filters = [license, publish_time, journal, authors]
    names = ['license', 'publish_time', 'journal', 'authors']
    query = []
    for i in range(4):
        if filters[i] != None and filters[i] != []:
            if names[i] == 'publish_time':
                print(type(filters[i]), filters[i])
                query.append(match(names[i],filters[i]))
            else:
                if len(filters[i]) > 1:
                    query.append(keyword_match(names[i], filters[i]))
                else:
                    query.append(match(names[i],filters[i][0][0]))

    if len(query) == 0:
        query = {'query' : { 'match_all': {} }}
    else:
        query = {'query': {'bool': {'must': query}}}
    return query

def as_dict(paper, pars,scores=[], indices=[]):
    return {
        'cord_id': paper['cord_id'],
        'title': paper['title'],
        'abstract': paper['abstract'],
        'authors': paper['authors'],
        'journal': paper['journal'],
        'doin': paper['doin'],
	    'url': paper['url'],
	    'source': paper['source'],
        'license': paper['license'],
        'publish_time': paper['publish_time'],
        'ranked_paragraphs': [{
            'section': p[1][0],
            'text': p[1][1],
            'score': round(scores[i], 2) if len(scores) > 0 else -1.0,
            'spans': indices[i] if len(indices) > 0 else []
        } for i, p in enumerate(pars)]
    }

def get_search_results(page, SEARCH_SIZE, script_query):
    client=Elasticsearch('nlp-elasticsearch:9200')
    response = client.search(
        index="meta",
        body={
            "from": (page-1) * SEARCH_SIZE,
            "size": 10,
            "query": script_query,
            "_source": { "includes":["cord_id", "title", "abstract", "authors", "doin", "url", "source", "journal", "publish_time", "license", "title_abstract_embeddings"]}
             }
         )
    hits = response['hits']['hits']
    total = response['hits']['total']['value']
    papers = []
    for i in hits:
        papers.append(i['_source'])
    return papers, total


def get_vector(query):
    bc = BertClient(ip='nlp-bert')
    vector = bc.encode([query])[0].tolist()
    return vector

def get_vector_numpy(query):
    bc = BertClient(ip='nlp-bert')
    vector = bc.encode([query])[0]
    return vector

def get_relevant_span(
    tokens: list,
    corpus: list) -> list:
    """ Returns passages idx relevant to query in corpus.
    Indices is a list of lists of tuples (begin, end) delimiting passages
    that are relevant to searched tokens.
    """
    indices = []
    for text in corpus:
        local_indices = []
        for sentence in sent_tokenize(text):
            low_sent = sentence.lower()
            found = False
            for tok in tokens:
                if low_sent.find(tok.lower()) > -1:
                    found = True
                    break
            if found == True:
                begin = text.find(sentence)
                end = begin + len(sentence)
                local_indices.append((begin, end))
        indices.append(list(set(local_indices)))
    return indices

def get_paper(cord_id):
    client=Elasticsearch('nlp-elasticsearch:9200')
    response = client.search(
        index="meta",
        body={
            "query": {
                "constant_score": {
                    "filter": {
                        "term": {
                            "cord_id" : cord_id
                            }
                        }
                    }
                }
            }
        )
    return response['hits']['hits'][0]['_source']

def get_paragraphs_similarity(cord_id, query_vector):
        client=Elasticsearch('nlp-elasticsearch:9200')
        script = {
            "script_score": {
                "query": {
                    "constant_score": {
                        "filter": {
                            "term": {
                                "cord_id" : cord_id
                                }
                            }
                        }
                    },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, doc['paragraph_embeddings']) + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
        response = client.search(
            index="paragraphs",
            body={
                "query": script,
            }
        )
        return response['hits']['hits']


