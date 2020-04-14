from dataclasses import dataclass, field
from pathlib import Path
from elasticsearch import Elasticsearch
import logging
from tqdm import tqdm
import pandas as pd
import pickle

# TODO this should be moved in a shared file
logging.basicConfig(level=logging.DEBUG)
# Mainly inspired by https://github.com/t0m-R/covid19-search-engine/blob/master/py/create_documents.py

@dataclass
class ElasticSearchProvider:
    # a DataFrame containg all the infos about the papers
    metafile: pd.DataFrame 
    # or a generator -> how to set generator type on fields ?
    embeddings: tuple = field(default_factory=list) # tuple of embeddings, (abstract, paragram)
    client: Elasticsearch = Elasticsearch()
    doc: dict = field(default_factory=dict)
    
    def load_meta(self):
        docs = []
        df = self.metafile
        for row in df.iterrows():
            series = row[1]
            doc = {
                'title': str(series.title),
                'abstract': str(series.abstract),
                'authors': str(series.authors),
                'doi': str(series.doi)
            }
            # REVIEW could yield but the csv is not that big
            docs.append(doc)
        return docs

    def create_document(self, doc: dict, abstract_emb: list, paragraph_emb: list, index_name: str = 'covid-19'):
        return {
            '_op_type': 'index',
            '_index': index_name,
            'abstract': doc['abstract'],
            'authors': doc['authors'],
            'doi': doc['doi'],
            'title': doc['title'],
            'abstract_emb': emb,
            'paragraph_emb': emb

        }


    def create_documents(self, out_path: Path, index_name: str = 'covid-19'):
        for doc, (abstract_emb, paragraph_emb) in zip(docs, self.embeddings):
            d = self.create_document(doc, abstract_emb, paragraph_emb, index_name)
            self.doc = {**doc, **d}

            # TODO write to disk each time is blocking and slow

    def create_index(self, index_path:Path, index_name: str = 'covid-19'):
        """Fill up elastic search
        
        :param index_path: [description]
        :type index_path: Path
        :param index_name: [description], defaults to 'covid-19'
        :type index_name: str, optional
        """
        # TODO add option to remove
        client.indices.delete(index=index_name, ignore=[404])
        client.indices.create(index=index_name, body=self.doc)


    def __call__(self, out_path:Path, index_name: str = 'covid-19'):
        bar = tqdm.bar(total=3)
        bar.set_description(f'Reading metafile from {self.metapath}...')
        bar.update()
        docs = self.load_meta()
        bar.set_description('Building documents...')
        self.create_documents(output_path, index_name)
        bar.set_description(f'Creating index from {out_path} with name={index_name}...')
        f.write(json.dumps(self.doc))
        self.create_index(out_path, index_name)
        bar.update()
        bar.set_description('Done!')


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
        print(len(entries))
        logging.info(f'Loading entries from {filepath} ...')
        for entry in tqdm(entries):
            if 'paragraphs' in entry:
                # TODO by @Francesco, we can iterate in paragraphs and create subdocuments linked to paragraphs
                entry['paragraphs'] = entry['paragraphs'][:100]
                entry['paragraphs_embeddings'] = entry[
                    'paragraphs_embeddings'][:100]

            yield entry 


for entry in ElasticSearchProvider.from_pkl(Path('../data/db_entries2.pkl')):
    print(entry)
    break

# df = pd.read_csv(Path('../data/metadata.csv'), nrows=100)



# elastic_provider = ElasticSearchProvider(df, [])

# elastic_provider.metafile.info()