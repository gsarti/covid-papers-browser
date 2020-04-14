from dataclasses import dataclass, field
from pathlib import Path
from elasticsearch import Elasticsearch
import logging
from tqdm import tqdm
import pandas as pd
import pickle
import json
from elasticsearch.helpers import bulk

# TODO this should be moved in a shared file
logging.basicConfig(level=logging.DEBUG)
# Mainly inspired by https://github.com/t0m-R/covid19-search-engine/blob/master/py/create_documents.py

@dataclass
class ElasticSearchProvider:
    """ 
    This class fills up elasticsearch using a common interface. This is convenient since one can define a custom classmethod
    for a custom data source. E.g. if you want to directly use a model to create the embeddings
    ```
    class MyElasticSearchProvider(ElasticSearchProvider):
        @classmethod
        def from_transformers_model(cls, model, datas):
            for data in datas:
                title_emb = model(data['title'])
                yield { 'title' : data['title], ..., 'title_abstract_embeddings' : title_emb }
    ```
    The ouput must be a iterable composed by dict with the following keys:

    TODO keys must be reviewed with @Gabriele

    ```
    cord_id', 'url', 'sha', 'title', 'source', 'doi', 'pmc_id', 'pubmed_id', 'license', 'abstract', 'publish_time', 'authors', 'journal', 'microsoft_id', 'who_id', 'paragraphs', 'bibliography', 'title_abstract_embeddings', 'paragraphs_embeddings
    ```
    """
    entries: list()
    index_file:  dict
    client: Elasticsearch = Elasticsearch()
    doc: list  = field(default_factory=list)
    # add index

    def create_documents(self, out_path: Path, index_name: str = 'covid-19'):
        for entry in tqdm(self.entries):
            entry_elastic  = {**entry, **{ '_op_type': 'index', '_index': index_name}}
            # TODO this can become huge!
            self.doc.append(entry_elastic)

    def create_index(self, index_path:Path, index_name: str = 'covid-19'):
        """Fill up elastic search
        
        :param index_path: [description]
        :type index_path: Path
        :param index_name: [description], defaults to 'covid-19'
        :type index_name: str, optional
        """
        # TODO add option to remove
        self.client.indices.delete(index=index_name, ignore=[404])
        self.client.indices.create(index=index_name, body=self.index_file) 


    def __call__(self, out_path:Path, index_name: str = 'covid-19'):
        """In order

        - [ ] create all the documents
        - [ ] create a new index from the document
        
        :param out_path: [description]
        :type out_path: Path
        :param index_name: [description], defaults to 'covid-19'
        :type index_name: str, optional
        """

        self.create_documents(out_path, index_name)

        logging.info(f'Creating index from {out_path} with name={index_name}...')
        self.create_index(out_path, index_name)
        bulk(self.client, self.doc)
        # with open(out_path, 'w') as f:
        #     f.write(json.dumps(self.doc))

    @classmethod
    def from_pkls(cls, root: Path, *args, **kwars):
        """Fill up elastic search from dir with .pkl files
        :param root: Root of the folder that contains the pickle files
        :type root: Path
        """
        filepaths = list(root.glob('**/*.pkl'))
        logging.info(f'Found {len(filepaths)} files in {root}')

        with open(fname, 'rb') as f:
            entries = pickle.load(f)
        pass

    @classmethod
    def from_pkl(cls, filepath: Path, *args, **kwars):
        """Fill up elastic search from a single pkl file
        
        :param filepath: Path to a pickle file
        :type filepath: Path
        """
        with open(filepath, 'rb') as f:
            entries = pickle.load(f)

        logging.info(f'Loading entries from {filepath} ...')
        def _stream():
            for entry in tqdm(entries[:5]):
                if 'paragraphs' in entry:
                    # TODO by @Francesco, we can iterate in paragraphs and create subdocuments linked to paragraphs
                    entry['paragraphs'] = entry['paragraphs'][:100]
                    entry['paragraphs_embeddings'] = entry[
                        'paragraphs_embeddings'][:100]
                tmp = {'title': entry['title'], 'doi': entry['doi'],  
                'abstract' : entry['abstract'],  }
                yield tmp 

        return cls(_stream(), *args, **kwars)

        


# elastic_provider = ElasticSearchProvider.from_pkl(Path('../data/db_entries2.pkl'))
index_file = {
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  },
  "mappings": {
    "dynamic": "true",
    "_source": {
      "enabled": "true"
    },
    "properties": {
      "title": {
        "type": "text"
      },
      "abstract": {
        "type": "text"
      },
      "doi": {
        "type": "text"
      },

    }
  }
}

# embedding dim = 768
elastic_provider = ElasticSearchProvider.from_pkl(Path('../data/db_entries2.pkl'),  index_file=index_file)

# elastic_provider = ElasticSearchProvider([{
#     'title' : 'title', 
#     'abstract': 'foo', 
#     'doi' : 'asd'}], index_file=index_file)

elastic_provider(out_path=Path('../data/elastic.json'))

# df = pd.read_csv(Path('../data/metadata.csv'), nrows=100)



# elastic_provider = ElasticSearchProvider(df, [])

# elastic_provider.metafile.info()