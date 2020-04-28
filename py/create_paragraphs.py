import pickle
import json
import argparse
from tqdm import tqdm


def create_document(doc, index_name):
    paragraphs = []
    paragraphs_embeddings = []
    for i in range(len(doc['paragraphs'])):
        paragraphs.append({'paragraph': doc['paragraphs'][i][1]})
        paragraphs_embeddings.append({'embedding': doc['paragraphs_embeddings'][i]})
    return {
        '_op_type': 'index',
        '_index': index_name,
        'cord_id': doc['cord_id'],
	    'paragraphs': paragraphs,
	    'paragraphs_embeddings': paragraphs_embeddings
    }

def info_paragraphs(doc, i, index_name):
    return {
        'len_pars': len(doc['paragraphs']),
        'type_pars': type(doc['paragraphs']),
        'type_par' : type(doc['paragraphs'][0]),
        'par0': doc['paragraphs'][i][0],
        'par1' : doc['paragraphs'][i][1]
    }

def create_paragraphs(doc, i, index_name):
    return {
        '_op_type': 'index',
        '_index': index_name,
        'cord_id': doc['cord_id'],
        'n_par': i,
        'par_title': doc['paragraphs'][i][0],
	    'paragraph': doc['paragraphs'][i][1],
	    'paragraph_embeddings': doc['paragraphs_embeddings'][i]
    }

def paragraphStat(parslist):
    nulls = 0
    n = 0
    ids = [0]
    c = 0
    counts = []
    for i, doc in enumerate(parslist):
        if len(doc['paragraphs']) > 0:
            if len(doc['paragraphs']) > 100:
                c+=100
            else:
                c +=len(doc['paragraphs'])
        else:
            nulls+=1
        if c >= 50000:
            n += c
            counts.append(c)
            ids.append(i+1)
            c = 0
    counts.append(c)
    return n, ids, counts, nulls

def load_dataset(path):
    with open(path, 'rb') as f:
        pkl = pickle.load(f)
    return pkl

def save_pars(docs, save, i, total):
    with tqdm(total=total, desc="        "+str(i+1)) as pbar:
        with open(save, 'a+') as f:
            for doc in docs:
                    if len(doc['paragraphs']) > 0:
                        if len(doc['paragraphs']) > 100:
                            stop = 100
                        else:
                            stop = len(doc['paragraphs'])
                        for i in range(stop):
                            d = create_paragraphs(doc, i, args.index_name)
                            f.write(json.dumps(d) + '\n')
                            pbar.update(1)

def main(args):
    "Loading pickle.."
    docs = load_dataset(args.pickle)
    n = str(args.counter)
    total, ids, counts, nulls = paragraphStat(docs)
    print("Processing ", str(total), "paragraphs of", str(len(docs)), "documents, leaving out", str(nulls), "documents without paragraphs.")
    print("Chunks:", len(ids))
    for i in range(len(ids)-1):
        save = 'data/index/paragraphs/'+args.index_name+str(n)+'-'+str(i)+'.index'
        start = ids[i]
        stop = ids[i+1]
        save_pars(docs[start:stop],save,i,counts[i])
    i = len(ids)
    save = 'data/'+args.index_name+str(n)+'-'+str(i)+'.index'
    save_pars(docs[ids[-1]:], save, i-1, counts[-1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing elasticsearch documents.')
    parser.add_argument('--pickle', required=True, help='pickle')
    parser.add_argument('--index_name', required=True, help='Elasticsearch index name.')
    parser.add_argument('--counter', '-c', required=True, help='Index counter for batch pickles')
    args = parser.parse_args()
    main(args)
