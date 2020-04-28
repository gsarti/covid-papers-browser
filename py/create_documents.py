import argparse
import json
import pandas as pd
from bert_serving.client import BertClient
bc = BertClient(output_fmt='list', check_length=False)


def create_document(doc, emb, index_name):
    return {
        '_op_type': 'index',
        '_index': index_name,
        'abstract': doc['abstract'],
	    'authors': doc['authors'],
	    'doi': doc['doi'],
        'title': doc['title'],
        'text_vector': emb
    }


def load_dataset(path):
    docs = []
    df = pd.read_csv(path)
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


def bulk_predict(docs, batch_size=128):
    """Predict bert embeddings."""
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i: i+batch_size]
        embeddings = bc.encode([doc['abstract'] for doc in batch_docs])
        for emb in embeddings:
            yield emb


def main(args):
    docs = load_dataset(args.data)
    save = args.data.split('.')[0]+'.index'
    with open(save, 'w') as f:
        for doc, emb in zip(docs, bulk_predict(docs,int(args.batch_size))):
            d = create_document(doc, emb, args.index_name)
            f.write(json.dumps(d) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating elasticsearch documents.')
    parser.add_argument('--data', help='data for creating documents.')
    parser.add_argument('--index_name', required=True, help='Elasticsearch index name.')
    parser.add_argument('--batch_size', default=128, help='batch of seqs')
    args = parser.parse_args()
    main(args)
