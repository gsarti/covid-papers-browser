""" Provides utility methods for performing semantic similarity retrieval."""

import numpy as np
from scipy.spatial.distance import cdist
from sentence_transformers import models, SentenceTransformer


def load_sentence_transformer(
    name: str = 'gsarti/scibert-nli', 
    max_seq_length: int  = 128, 
    do_lower_case: bool  = True) -> SentenceTransformer:
    """ Loads a SentenceTransformer from HuggingFace AutoModel bestiary """
    word_embedding_model = models.BERT(
            'gsarti/scibert-nli',
            max_seq_length=128,
            do_lower_case=True
        )
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
            pooling_mode_mean_tokens=True,
            pooling_mode_cls_token=False,
            pooling_mode_max_tokens=False
        )
    return SentenceTransformer(modules=[word_embedding_model, pooling_model])

def match_query_paragraphs(
    query: str,
    model: SentenceTransformer,
    idx: list,
    corpus_embed: list,
    top_k: int = 5):
    """ Matches query and paragraph embeddings, returning top scoring paragraphs ids and scores """
    query_embed = model.encode([query], show_progress_bar=False)[0].reshape(1,-1)
    distances = 1 - cdist(query_embed, corpus_embed, "cosine")
    results = zip(idx, distances.reshape(-1,1))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results[:top_k]