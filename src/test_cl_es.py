from searchers import Elasticsearcher
from embedders import TransformerEmbedder
from covid_browser import load_sentence_transformer

searcher = Elasticsearcher()

embedder = TransformerEmbedder.from_name('gsarti/scibert-nli')

while True:
    query = input('Search for:')
    emd = embedder(query).tolist()[0]
    res = searcher(emd)
    hits = res['hits']['hits']
    [print(f"\t{hit['_source']['title']}") for hit in hits]

