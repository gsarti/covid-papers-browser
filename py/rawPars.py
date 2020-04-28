import pickle
import argparse
from tqdm import tqdm
import gc

def load_pickle(file):
    print('Loading pickle..')
    with open(file, 'rb') as f:
        entry = pickle.load(f)
    return entry

def save_pars(pars, c, i):
    paragraphs = []
    total = len(pars)
    for paper in pars:
        p = { 'cord_id': paper['cord_id'], 'paragraphs': paper['paragraphs'], 'paragraphs_embeddings': paper['paragraphs_embeddings']  }
        paragraphs.append(p)
    save = f'data/pickle/paragraphs/paragraphs{c}-{i+1}.pkl'
    print(f'Saving {save}..')
    with open(save, 'wb') as f:
        pickle.dump(paragraphs, f)
    del paragraphs
    del pars
    gc.collect()

def main(args):

    paragraphs = []
    entry = load_pickle(args.pickle)
    c = args.counter
    i=0
    if len(entry) > 2500:
        print("Pickle is huge, splitting in half..")
        mid = len(entry)//2
        half1 = entry[:mid]
        del entry
        gc.collect()
        save_pars(half1, c, i)
        i +=1
        gc.collect()
    if i>0:
        tmp = load_pickle(args.pickle)
        entry = tmp[mid:]
        del tmp
        gc.collect()
    save_pars(entry, c, i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing elasticsearch documents.')
    parser.add_argument('--pickle', required=True, help='pickle')
    parser.add_argument('--counter', '-c', required=True, help='Index counter for batch pickles')
    args = parser.parse_args()
    main(args)
