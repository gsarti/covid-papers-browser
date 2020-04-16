import spacy
from sentence_transformers import SentenceTransformer
import numpy as np
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
    def __init__(self, model: SentenceTransformer):
        self.model = model

    def embed(self, query: str) -> np.array:
        query_emb = self.model.encode([query], show_progress_bar=False)[0].reshape(1,-1)
        return query_emb
