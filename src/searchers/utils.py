import spacy

class Embedder:
    def process(self, query):
        return query
    
    def embed(self, query):
        raise NotImplementedError

    def __call__(self):
        query_pre = self.preprocess(query)
        query_emb = self.embed(query_pre)
        return query_emb


class TransformerEmbedder(Embedder):
    def __init__(self, model: SentenceTransformer)
        nlp = spacy.load("en_core_web_sm")

    def preprocess(self, query: str):
        query_pre =  nlp(query)
        return query_pre

    def embed(self, query: str):
        query_emb = model.encode([query], show_progress_bar=False)[0].reshape(1,-1)
        return query_emb
