import pickle
import json
import argparse

def create_document(doc, index_name):
    if doc['publish_time'] == "":
        time = "1900-01-01"
    else:
        time = doc['publish_time']
    return {
        '_op_type': 'index',
        '_index': index_name,
        'cord_id': doc['cord_id'],
        'title': doc['title'],
	    'abstract': doc['abstract'],
        'authors': doc['authors'],
        'journal': doc['journal'],
        'doin': doc['doin'],
        'url': doc['url'],
        'source': doc['source'],
        # date cannot be NULL
        'publish_time': time,
        'license': doc['license'],
        'title_abstract_embeddings': doc['title_abstract_embeddings']
    }

def load_dataset(path):
    with open(path, 'rb') as f:
        pkl = pickle.load(f)
    return pkl

def get_missing(dataset, id):
    doc = list(filter(lambda x: x ['cord_id'] == id, dataset))
    if len(doc) > 0:
        for k, v  in doc[0].items():
            if v == None:
                doc[0][k] = ""
        return doc[0]
    else:
        return None

def main(args):
    docs = load_dataset(args.pickle)
    with open ('data/json/fix_meta.json', 'r') as f:
        fix = json.load(f)
    save = 'data/index/meta.index'
    with open(save, 'w') as f:
        for doc in docs:
            missing = get_missing(fix, doc['cord_id'])
            if missing != None:
                doc['doin'] = missing['doin']
                doc['url'] = missing['url']
                doc['source'] = missing['source']
                d = create_document(doc, args.index_name)
                f.write(json.dumps(d) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing elasticsearch documents.')
    parser.add_argument('--pickle', required=True, help='pickle')
    parser.add_argument('--index_name', required=True, help='Elasticsearch index name.')
    args = parser.parse_args()
    main(args)
