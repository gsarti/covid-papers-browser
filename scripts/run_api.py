import os
import sys
import argparse
import numpy as np
from flask import Flask, request, json
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'src'))

from covid_browser import load_sentence_transformer, match_query, PaperOverview, PaperDetails

parser = argparse.ArgumentParser()
parser.add_argument(
    "--db_name", 
    default="coviddb", 
    type=str, 
    required=False,
    help="Mongo database name."
)
parser.add_argument(
    "--collection_name", 
    default="cord19scibert", 
    type=str, 
    required=False,
    help="Mongo collection name."
)
parser.add_argument(
    "--model_name", 
    default="gsarti/scibert-nli", 
    type=str, 
    required=False,
    help="One among the models supported by HuggingFace AutoModel (e.g. `gsarti/scibert-nli`)"
)
args = parser.parse_args()
app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://localhost:27017/{args.db_name}"
mongo = PyMongo(app)
col = mongo.db[args.collection_name]
model = load_sentence_transformer(name=args.model_name)
papers, embeddings = zip(*[
    (
        PaperOverview(x),
        np.array(x['title_abstract_embeddings'])
    ) 
    for x in col.find({}, {
        '_id': 0,
        'cord_id': 1,
        'title': 1,
        'journal': 1,
        'authors': 1,
        'abstract': 1,
        'title_abstract_embeddings': 1
    })]
)
papers, embeddings = list(papers), list(embeddings)


@app.route("/")
@app.route("/help")
def help():
    return "Interrogate the Covid-19 Semantic Browser API as follows: TODO"


@app.route("/paper")
def get_papers():
    count = request.args.get('count', default = 10, type = int)
    query = request.args.get('query', default = None, type = str)
    if query is not None:
        match = match_query(query, model, papers, embeddings, count)
        results = [tup[0].as_dict() for tup in match]
        return json.jsonify(results)
    else:
        return 'A query must be specified!'


@app.route("/paper/<id>")
def get_paper_by_id(id):
    count = request.args.get('count', default = 10, type = int)
    query = request.args.get('query', default = None, type = str)
    x = col.find_one({'cord_id': id})
    if x is not None:
        paper = PaperDetails(x)
        if query is not None:
            match = match_query(query, model, paper.paragraphs, paper.paragraphs_embeddings, count)
            paper.ranked_paragraphs = [tup[0] for tup in match]
        return paper.as_dict()
    else:
        return 'Document not found!'


if __name__ == "__main__":
    app.run(debug=True)