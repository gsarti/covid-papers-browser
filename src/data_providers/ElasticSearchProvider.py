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
logging.basicConfig(level=logging.INFO)
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
    index_file: dict
    client: Elasticsearch = Elasticsearch()
    doc: list = field(default_factory=list)
    index_name: str = 'covid-19'

    def create_and_bulk_documents(self, batch_size: int = 128):

        for entry in tqdm(self.entries):
            entry_elastic = {
                **entry,
                **{
                    '_op_type': 'index',
                    '_index': self.index_name
                }
            }

            self.doc.append(entry_elastic)
            should_bulk = len(current_batch) >= batch_size
            if should_bulk:
                bulk(self.client)
                self.doc = []

    def create_index(self):
        """Fill up elastic search
        """
        self.client.indices.create(index=self.index_name, body=self.index_file)

    def load(self, file_path: Path):
        """Load a file that contains the documents indeces
      
      :param file_path: [description]
      :type file_path: Path
      """
        with open(file_path, 'r') as f:
            self.doc = json.load(f)

    def drop(self):
        """Drop the current index
        """
        self.client.indices.delete(index=self.index_name, ignore=[404])

    def __call__(self, batch_size: int = 128):
        """In order

        - [ ] create all the documents
        - [ ] create a new index from the document
        
        """
        self.drop()
        logging.info(f'Creating index {self.index_name}...')
        self.create_index()
        logging.info(f'Creating documents...')
        self.create_and_bulk_documents(batch_size)

        return self

    def save(self, out_path: Path):
        with open(out_path, 'w') as f:
            f.write(json.dumps(self.doc))

    @classmethod
    def from_pkls(cls, root: Path, _paragraphs: int = 100, *args, **kwars):
        """Fill up elastic search from dir with .pkl files
        :param root: Root of the folder that contains the pickle files
        :type root: Path
        """
        filepaths = list(root.glob('**/*.pkl'))
        logging.info(f'Found {len(filepaths)} files in {root}')

        providers = []

        for file_path in filepaths:
            try:
                provider = cls.from_pkl(file_path, *args, **kwars)
                providers.append(provider)
            except Exception as e:
                logging.warning(f'Error {e} when processing file={file_path}')

        return providers

    @classmethod
    def from_pkl(cls, filepath: Path, n_paragraphs: int = 100, *args, **kwars):
        """Fill up elastic search from a single pkl file
        
        :param filepath: Path to a pickle file
        :type filepath: Path
        """
        with open(filepath, 'rb') as f:
            entries = pickle.load(f)

        logging.info(f'Loading entries from {filepath} ...')

        def _stream():
            for entry in tqdm(entries):
                if 'paragraphs' in entry:
                    # TODO by @Francesco, we can iterate in paragraphs and create subdocuments linked to paragraphs
                    entry['paragraphs'] = entry['paragraphs'][:5]
                    entry['paragraphs_embeddings'] = entry[
                        'paragraphs_embeddings'][:n_paragraphs]

                yield entry

        return cls(_stream(), *args, **kwars)


if __name__ == '__main__':
    with open('./data/es_index.json', 'r') as f:
        index_file = json.load(f)

        es_providers = ElasticSearchProvider.from_pkls(root=Path('./data'),
                                                       index_file=index_file)
        for i, es_provider in enumerate(es_providers):
            es_provider()
            del es_provider

    # # es_provider = ElasticSearchProvider.from_pkl(
    # #     Path('./data/db_entries2.pkl'), index_file=index_file)
    # es_provider().save(Path('./data/elastic.json'))
