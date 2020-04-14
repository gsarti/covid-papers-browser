from dataclasses import dataclas
from pathlib import Path
from elasticsearch import Elasticsearch
import logging
from tqdm import tqdm

# Mainly inspired by https://github.com/t0m-R/covid19-search-engine/blob/master/py/create_documents.py

@dataclass
class ElasticSearchBuilder:
    metapath: Path 
    # or a generator -> how to set generator type on fields ?
    embeddings: list = field(default_factory=list)
    client: Elasticsearch = Elasticsearch()
    doc: dict = field(default_factory=dict)
    
    def load_meta(self):
        docs = []
        df = pd.read_csv(self.metapath)
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

    def create_document(self, doc: dict, emb: str, index_name: str = 'covid-19'):
        return {
            '_op_type': 'index',
            '_index': index_name,
            'abstract': doc['abstract'],
            'authors': doc['authors'],
            'doi': doc['doi'],
            'title': doc['title'],
            'text_vector': emb
        }


    def create_documents(self, out_path: Path, index_name: str = 'covid-19'):
            with open(out_path, 'w') as f:
            for doc, emb in zip(docs, self.embeddings):
                d = self.create_document(doc, emb, index_name)
                self.doc = {***doc, **d}

                # TODO write to disk each time is blocking and slow
                f.write(json.dumps(d) + '\n')


    def create_index(self, index_path:Path, index_name: str = 'covid-19'):
        """Fill up elastic search
        
        :param index_path: [description]
        :type index_path: Path
        :param index_name: [description], defaults to 'covid-19'
        :type index_name: str, optional
        """
        client.indices.delete(index=index_name, ignore=[404])
        client.indices.create(index=index_name, body=self.doc)



    def __call__(self, out_path:Path, index_name: str = 'covid-19'):
        bar = tqdm.bar(total=3)
        bar.set_description('Reading metafile from {self.metapath}...')
        bar.update()
        docs = self.load_meta()
        bar.set_description('Building documents...')
        self.create_documents(output_path, index_name)
        bar.set_description('Creating index from {out_path} with name={index_name}...')
        f.write(json.dumps(self.doc))
        self.create_index(out_path, index_name)
        bar.update()
        bar.set_description('Done!')


    @classmethod
    def from_pkls(cls, root: Path):
        """Fill up elastic search from dir with .pkl files
        
        :param root: Root of the folder that contains the pickle files
        :type root: Path
        """
        pass

    @classmethod
    def from_pkl(cls, filepath: Path):
        """Fill up elastic search from a single pkl file
        
        :param filepath: Path to a pickle file
        :type filepath: Path
        """
        pass