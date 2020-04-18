""" Provides utility methods used in scripts."""

import os
import json
import numpy as np
from scipy.spatial.distance import cdist
from nltk.tokenize import sent_tokenize
from sentence_transformers import models, SentenceTransformer
from .paper import PaperDatabaseEntryDetails, PaperDatabaseEntryOverview

MAX_PARAGRAPH_COUNT = 100 # Max # of paragraphs per section

def load_sentence_transformer(
    name: str = 'gsarti/scibert-nli', 
    max_seq_length: int  = 128, 
    do_lower_case: bool  = True) -> SentenceTransformer:
    """ Loads a SentenceTransformer from HuggingFace AutoModel bestiary """
    word_embedding_model = models.BERT(
            'gsarti/biobert-nli',
            max_seq_length=128,
            do_lower_case=True
        )
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
            pooling_mode_mean_tokens=True,
            pooling_mode_cls_token=False,
            pooling_mode_max_tokens=False
        )
    return SentenceTransformer(modules=[word_embedding_model, pooling_model])


def match_query(
    query: str,
    model: SentenceTransformer,
    corpus: list,
    corpus_embed: list) -> list:
    """ Matches query and paragraph embeddings, returning top scoring paragraphs ids and scores """
    query_embed = model.encode([query], show_progress_bar=False)[0].reshape(1,-1)
    distances = 1 - cdist(query_embed, corpus_embed, "cosine")
    distances = [d for dist in distances.reshape(-1,1).tolist() for d in dist]
    assert len(distances) == len(corpus)
    results = list(zip(corpus, distances))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results


def create_db_entry(
    data_path: str,
    csv_entry: dict, 
    model: SentenceTransformer,
    data_type):
    """ Creates a single DB entry of specified type from a csv entry using the model"""
    db_entry = data_type(csv_entry)
    db_entry.compute_title_abstract_embeddings(model)
    if (csv_entry['has_pdf_parse'] == True
        and data_type == PaperDatabaseEntryDetails
        and db_entry.abstract != ''):

        foldername = csv_entry['full_text_file']
        # Format is e.g. 'data/biorxiv_medrxiv/biorxiv_medrxiv/file.json'
        path = os.path.join(data_path, foldername, 'pdf_json', f'{db_entry.sha}.json')
        file = json.load(open(path, 'r'))
        paragraphs = []
        # Order is: abstracts, body, back_matter, ref_entries
        parts = [file['abstract'], file['body_text'], file['back_matter']]
        for part in parts:
            for paragraph in part:
                paragraphs.append((paragraph['section'], paragraph['text']))
        for key, paragraph in file['ref_entries'].items():
            paragraphs.append((paragraph['type'].title(), paragraph['text']))
        db_entry.paragraphs = paragraphs[:MAX_PARAGRAPH_COUNT]
        db_entry.compute_paragraphs_embeddings(model)
        db_entry.bibliography = [file['bib_entries'][entry] for entry in file['bib_entries']]
    return db_entry


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
