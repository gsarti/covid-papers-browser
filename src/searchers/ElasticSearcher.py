from elasticsearch import Elasticsearch
from dataclasses import dataclass


@dataclass
class Elasticsearcher:
    client: Elasticsearch = Elasticsearch()
    preprocess: callable = lambda x: x

    def __call__(self, query):
        query_pre = preprocess(query)
        script_query = {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source":
                    "cosineSimilarity(params.query_vector, doc['title_abstract_embeddings']) + 1.0",
                    "params": {
                        "query_vector": query_pre
                    }
                }
            }
        }

        response = client.search(
            index=INDEX_NAME,
            body={
                "size": SEARCH_SIZE,
                "query": script_query,
                "_source": {
                    "includes":
                    # TODO ask @Gabriele
                    ["title", "abstract", "authors", "doi"]
                }
            })

