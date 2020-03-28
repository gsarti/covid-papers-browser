import os
import sys
import json
import logging
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'src'))

from covid_browser import load_sentence_transformer, PaperDatabaseEntry

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logging.basicConfig(level=logging.INFO)


def create_db_entry(
    csv_entry: dict, 
    model: SentenceTransformer) -> PaperDatabaseEntry:
    """ Creates a single DB entry from a csv entry using the model for creating embeddings """
    db_entry = PaperDatabaseEntry(csv_entry)
    db_entry.compute_title_abstract_embeddings(model)
    if csv_entry['has_full_text'] == True:
        foldername = csv_entry['full_text_file']
        # Format is e.g. 'data/biorxiv_medrxiv/biorxiv_medrxiv/file.json'
        path = os.path.join('data', foldername, foldername, f'{db_entry.sha}.json')
        file = json.load(open(path, 'r'))
        paragraphs = []
        # Order is: abstracts, body, back_matter, ref_entries
        parts = [file['abstract'], file['body_text'], file['back_matter']]
        for part in parts:
            for paragraph in part:
                paragraphs.append((paragraph['section'], paragraph['text']))
        for key, paragraph in file['ref_entries'].items():
            paragraphs.append((paragraph['type'].title(), paragraph['text']))
        db_entry.paragraphs = paragraphs
        db_entry.compute_paragraphs_embeddings(model)
        db_entry.bibliography = [file['bib_entries'][entry] for entry in file['bib_entries']]
    return db_entry


def create_db(
    data_path: str = 'data/metadata.csv',
    db_name: str = 'coviddb',
    collection_name: str = 'cord19scibert',
    model_name: str = 'gsarti/scibert-nli') -> None:
    """ Creates a new Mongo database with entries from data_path, using model model_name """
    model = load_sentence_transformer(name=model_name)
    df = pd.read_csv(data_path)
    df = df.fillna('')
    db_entries = []
    for _, row in tqdm(df.iterrows()):
        db_entry = create_db_entry(row, model)
        # Only add entries with at least one between title and abstract to enable search
        if len(db_entry.title_abstract_embeddings) > 0:
            db_entries.append(db_entry.as_dict())
    client = MongoClient()
    db = client[db_name]
    col = db[collection_name]
    col.insert_many(db_entries)
    logger.info(f'Done: {len(db_entries)} new.')


def update_db(
    old_data_path: str = 'data/metadata_old.csv',
    data_path: str = 'data/metadata.csv',
    db_name: str = 'coviddb',
    collection_name: str = 'cord19scibert',
    model_name: str = 'gsarti/scibert-nli') -> None:
    """ Updates the DB entries based on old_data_path dataframe with new ones based on
    data_path, inserting new items and updating the ones that are already present.
    """
    model = load_sentence_transformer(name=model_name)
    df_old = pd.read_csv(old_data_path)
    df_old = df_old.fillna('')
    df_new = pd.read_csv(data_path)
    df_old = df_old.fillna('')
    if not df_new.equals(df_old):
        modified_new = df_new.merge(
            df_old,
            how='left', 
            indicator=True
        ).loc[lambda f: f['_merge']=='left_only']
        db_entries = []
        logger.info(f'Total new or updated entries: {len(modified_new)}')
        for _, row in tqdm(modified_new.iterrows()):
            db_entry = create_db_entry(row, model)
            # Only add entries with at least one between title and abstract to enable search
            if len(db_entry.title_abstract_embeddings) > 0:
                db_entries.append(db_entry.as_dict())
        client = MongoClient()
        db = client[db_name]
        col = db[collection_name]
        new_elements = []
        replaced_count = 0
        for entry in db_entries:
            # Replace document if found, else it inserts it
            val = col.find_one_and_replace(
                {'cord_id': entry['cord_id']},
                entry,
                upsert=True
            )
            if val is not None:
                replaced_count += 1
        inserted_count = len(db_entries) - replaced_count
        logger.info(f'Done: {replaced_count} modified, {inserted_count} new.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path", 
        default="data/metadata.csv", 
        type=str, 
        required=False,
        help="Dataset path where entries can be found."
    )
    parser.add_argument(
        "--db_name", 
        default="coviddb", 
        type=str, 
        required=False,
        help="Mongo database name."
    )
    parser.add_argument(
        "--collection_name", 
        default="cord19scibert", 
        type=str, 
        required=False,
        help="Mongo collection name."
    )
    parser.add_argument(
        "--model_name", 
        default="gsarti/scibert-nli", 
        type=str, 
        required=False,
        help="One among the models supported by HuggingFace AutoModel (e.g. `gsarti/scibert-nli`)"
    )
    parser.add_argument(
        "--old_data_path", 
        default=None, 
        type=str, 
        required=False,
        help="Needed for updating operations, represent the current database entries before updating."
    )
    parser.add_argument(
        "--create", 
        action="store_true",
        help="Creates a new Mongo database."
    )
    parser.add_argument(
        "--update", 
        action="store_true",
        help="Updates an existing Mongo database."
    )
    args = parser.parse_args()
    if not (args.update != args.create): # XOR
        raise AttributeError('Exactly one among modes "create" and "update" must be selected.')
    if args.update and args.old_data_path is None:
        raise AttributeError('The parameter old_data_path must be specified when updating.')
    if args.create:
        create_db(
            data_path = args.data_path,
            db_name = args.db_name,
            collection_name = args.collection_name,
            model_name = args.model_name
        )
    elif args.update:
        update_db(
            old_data_path = args.old_data_path,
            data_path = args.data_path,
            db_name = args.db_name,
            collection_name = args.collection_name,
            model_name = args.model_name
        )
