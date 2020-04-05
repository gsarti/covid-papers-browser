import os
import sys
import argparse
import warnings
import spacy
import logging
import numpy as np
from collections import Counter
from flask import Flask, request, json, render_template
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask_cors import CORS

sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir,
                 'src'))
warnings.filterwarnings('ignore', category=FutureWarning)

from covid_browser import (load_sentence_transformer, match_query,
                           get_relevant_span, PaperOverview, PaperDetails)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--db_name", 
    default="covid",
    type=str, 
    required=False,
    help="Mongo database name."
)
parser.add_argument(
    "--overview_collection_name", 
    default="cord19scibertoverview", 
    type=str, 
    required=False,
    help="Mongo collection name."
)
parser.add_argument(
    "--details_collection_name", 
    default="cord19scibertdetails", 
    type=str, 
    required=False,
    help="Mongo collection name."
)
parser.add_argument(
    "--model_name", 
    default="gsarti/scibert-nli", 
    type=str, 
    required=False,
    help=
    "One among the models supported by HuggingFace AutoModel (e.g. `gsarti/scibert-nli`)"
)
args = parser.parse_args()
logging.info(f'args={args}')
app = Flask(__name__,
            template_folder=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), os.pardir,
                'templates'))
CORS(app)
app.config["MONGO_URI"] = os.environ.get(
    "MONGO_URI", f"mongodb://localhost:27017/{args.db_name}")
logging.info(f'MONGO_URI={app.config["MONGO_URI"]}')
# setup DB
mongo = PyMongo(app)
overview_col = mongo.db[args.overview_collection_name]
details_col = mongo.db[args.details_collection_name]
# #  indexing by cord_id to increase access speed
details_col.create_index('cord_id')
# index_name = 'cord_id'
# if index_name not in details_col.index_information():
#     details_col.create_index(index_name, unique=True)
# setup NLP models
model = load_sentence_transformer(name=args.model_name)
nlp = spacy.load("en_core_web_sm")
papers, embeddings, times, authors, journals, licenses = map(
    list,
    zip(*[(PaperOverview(x), np.array(x['title_abstract_embeddings']),
           x['publish_time'], x['authors'], x['journal'], x['license'])
          for x in overview_col.find({}, {
              '_id': 0,
              'cord_id': 1,
              'title': 1,
              'journal': 1,
              'authors': 1,
              'publish_time': 1,
              'license': 1,
              'abstract': 1,
              'title_abstract_embeddings': 1
          })]))
# Convert dates to years, flatten authors lists
times = [date.split('-')[0] for date in times if type(date) is str]
authors = [
    author for coautors in authors for author in coautors if author != ""
]
journals = [j for j in journals if j != '']
c_times, c_authors, c_journals, c_licenses = Counter(times), Counter(
    authors), Counter(journals), Counter(licenses)


@app.route("/")
@app.route("/help")
def help():
    return render_template('help.html')


@app.route("/years")
def get_years():
    count = request.args.get('count', default = 1000, type = int)
    return json.jsonify(c_times.most_common(count))


@app.route("/authors")
def get_authors():
    count = request.args.get('count', default = 1000, type = int)
    return json.jsonify(c_authors.most_common(count))


@app.route("/journals")
def get_journals():
    count = request.args.get('count', default = 1000, type = int)
    return json.jsonify(c_journals.most_common(count))


@app.route("/licenses")
def get_licenses():
    count = request.args.get('count', default = 1000, type = int)
    return json.jsonify(c_licenses.most_common(count))


@app.route("/paper", methods=['POST'])
def get_papers():
    print(request)
    count = request.get_json().get('count')
    if count is None:
        count=10
    query = request.get_json().get('query')
    score = request.get_json().get('score')
    if score is None:
        score=0.0
    p_years = request.get_json().get('year')
    if p_years is None:
        p_years=[]
    p_authors = request.get_json().get('author')
    if p_authors is None:
        p_authors=[]
    p_journals = request.get_json().get('journal')
    if p_journals is None:
        p_journals=[]
    p_licenses = request.get_json().get('license')
    if p_licenses is None:
        p_licenses=[]
    page = request.get_json().get('page')
    if page is None:
        page=1
    if query:
        match = match_query(query, model, papers, embeddings)
        match = [(m, s) for m, s in match if s > score]
        if len(p_years) > 0:
            match = [(m,s) for m,s in match if str(m.year) in [ str(p_year[0]) for p_year in p_years]]
        if len(p_authors) > 0:
            match = [(m,s) for m,s in match if any(a in m.authors for a in [ p_author[0] for p_author in p_authors])]
        if len(p_journals) > 0:
            match = [(m,s) for m,s in match if m.journal in [p_journal[0] for p_journal in p_journals]]
        if len(p_licenses) > 0:
            match = [(m,s) for m,s in match if m.license in [p_licence[0] for p_licence in p_licenses]]
        results = [paper.as_dict(score) for paper, score in match]
        return json.jsonify({ "total": len(results), "data": results[count*(page-1):count*page]} )
    else:
        return json.jsonify([])


@app.route("/singlearticle", methods=['POST'])
def get_paper_by_id():
    count = request.get_json().get('count')
    if count is None:
        count=10
    query = request.get_json().get('query')

    cord_id = request.get_json().get('cord_id')
    if cord_id is None:
        return {}

    score = request.get_json().get('score')
    if score is None:
        score=0.0
    x = details_col.find_one({'cord_id': cord_id})
    if x is not None:
        paper = PaperDetails(x)
        scores, indices = [], []
        if query is not None and len(paper.paragraphs) > 0:
            doc = nlp(query)
            match = match_query(query, model, paper.paragraphs,
                                paper.paragraphs_embeddings)
            paper.ranked_paragraphs, scores = map(
                list, zip(*[(p, s) for p, s in match if s > score][:count]))
            indices = get_relevant_span(
                [t.text for t in doc if not t.is_stop],
                [p for _, p in paper.ranked_paragraphs])
        return paper.as_dict(scores, indices)
    else:
        return {}


if __name__ == "__main__":
    # get enviroment variables
    env = os.environ.get('FLASK_ENV', 'development')
    port = os.environ.get('FLASK_PORT', 5000)
    debug = env == 'development'

    app.run(host="0.0.0.0", debug=debug, port=port)

