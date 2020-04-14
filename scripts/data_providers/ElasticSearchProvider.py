from dataclasses import dataclas
from pathlib import Path
from elasticsearch import Elasticsearch
import logging
from tqdm import tqdm

# Mainly inspired by https://github.com/t0m-R/covid19-search-engine/blob/master/py/create_documents.py

@dataclass
class ElasticSearchBuilder:
    metapath: Path 
    embeddings: list = field(default_factory=list)
    client: Elasticsearch = Elasticsearch()

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


    def create_index(self, index_path:Path, index_name: str = 'covid-19'):
        """Fill up elastic search
        
        :param index_path: [description]
        :type index_path: Path
        :param index_name: [description], defaults to 'covid-19'
        :type index_name: str, optional
        """
        client.indices.delete(index=args.index_name, ignore=[404])
        with open(index_path) as index_file:
            source = index_file.read().strip()
            client.indices.create(index=index_name, body=source)


    def create_documents(self, out_path: Path, index_name: str = 'covid-19'):
            with open(out_path, 'w') as f:
            for doc, emb in zip(docs, bulk_predict(docs,int(args.batch_size))):
                d = self.create_document(doc, emb, index_name)
                f.write(json.dumps(d) + '\n')


    def __call__(self, out_path:Path, index_name: str = 'covid-19'):
        bar = tqdm.bar(total=3)
        bar.set_description('Reading metafile from {self.metapath}...')
        bar.update()
        docs = self.load_meta()
        bar.set_description('Building documents...')
        self.create_documents(output_path, index_name)
        bar.set_description('Creating index from {out_path} with name={index_name}...')
        self.create(out_path, index_name)
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