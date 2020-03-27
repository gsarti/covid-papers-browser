import os
import sys
import numpy as np
from flask import Flask, request, json
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'src'))

from covid_browser import load_sentence_transformer, match_query_paragraphs

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/coviddb"
mongo = PyMongo(app)
col = mongo.db.cord19scibert

indices, embeddings = zip(
    *[(x['_id'], np.array(x['title_abstract_embeddings'])) 
    for x in col.find({}, {'title_abstract_embeddings':1})]
)
indices, embeddings = list(indices), list(embeddings)

@app.route("/")
@app.route("/help")
def help():
    return "Interrogate the Covid-19 Semantic Browser API as follows: TODO"


@app.route("/paper")
def get_papers():
    count = request.args.get('count', default = 10, type = int)
    query = request.args.get('query', default = None, type = str)
    if query is not None:
        model = load_sentence_transformer()
        match = match_query_paragraphs(query, model, indices, embeddings, count)
        results = []
        for x in col.find({'_id': {"$in": [id for id, score in match]}}):
            results.append({
                'id': str(x['_id']),
                'title': x['title'],
                'doi': x['doi'],
                'source': x['source'],
                'journal': x['journal'],
                'authors': x['authors'],
                'publish_time': x['publish_time'],
                'abstract': x['abstract']
            })
        return json.jsonify(results)
    else:
        return 'A query must be specified!'


@app.route("/paper/<id>")
def get_paper_by_id(id):
    x = col.find_one({'_id': ObjectId(id)})
    if x is not None:
        return {
                    'id': str(x['_id']),
                    'title': x['title'],
                    'doi': x['doi'],
                    'source': x['source'],
                    'journal': x['journal'],
                    'authors': x['authors'],
                    'publish_time': x['publish_time'],
                    'abstract': x['abstract']
                }
    else:
        return 'Document not found!'


if __name__ == "__main__":
    app.run(debug=True)