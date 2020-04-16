import spacy
import numpy as np
from sentence_transformers import SentenceTransformer
from covid_browser import load_sentence_transformer

class Embedder:
    def preprocess(self, query: str) -> np.array:
        return query
    
    def embed(self, query: str) -> np.array:
        raise NotImplementedError

    def __call__(self, query: str) -> np.array:
        query_pre = self.preprocess(query)
        query_emb = self.embed(query_pre)
        return query_emb

class TransformerEmbedder(Embedder):
    """Use a model from transformers to embed
    """
    def __init__(self, model: SentenceTransformer):
        self.model = model

    def embed(self, query: str) -> np.array:
        query_emb = self.model.encode([query], show_progress_bar=False)[0].reshape(1,-1)
        return query_emb
    
    @classmethod
    def from_name(cls, name: str, *args, **kwargs):
        model = load_sentence_transformer(name=name)
        return cls(model, *args, **kwargs)
