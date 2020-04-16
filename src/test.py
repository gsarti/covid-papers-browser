from searchers import Elasticsearcher
from embedders import TransformerEmbedder
from covid_browser import load_sentence_transformer

searcher = Elasticsearcher()

model = load_sentence_transformer(name='gsarti/scibert-nli')

embedder = TransformerEmbedder(model)
emd = embedder('Corona virus').tolist()
print(type(emd))
res = searcher(emd)

print(res)
