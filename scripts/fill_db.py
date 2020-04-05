import argparse
import pickle
from tqdm import tqdm
from pymongo import MongoClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_name",
                        default="covid",
                        type=str,
                        required=False,
                        help="Mongo database name.")
    parser.add_argument("--collection_name",
                        default="cord19scibertdetails",
                        type=str,
                        required=False,
                        help="Mongo collection name.")
    parser.add_argument(
        '-f',
        '--filename',
        action='append',
        required=True,
        help=
        "Filenames for .pkl files containing entries for filling the database."
    )
    args = parser.parse_args()
    client = MongoClient()
    db = client[args.db_name]
    col = db[args.collection_name]
    
    for fname in tqdm(args.filename):
        with open(fname, 'rb') as f:
            entries = pickle.load(f)

    for entry in tqdm(entries):
        if 'paragraphs' in entry:
            # TODO by @Francesco, we can iterate in paragraphs and create subdocuments linked to paragraphs
            entry['paragraphs'] = entry['paragraphs'][:100]
            entry['paragraphs_embeddings'] = entry[
                'paragraphs_embeddings'][:100]
    col.insert_many(entries)
