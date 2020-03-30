import os
import sys
import logging
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm
from pymongo import MongoClient

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir,
        'src'
    )
)

from covid_browser import (
    load_sentence_transformer,
    create_db_entry,
    PaperDatabaseEntryOverview,
    PaperDatabaseEntryDetails
)

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logging.basicConfig(level=logging.INFO)

TYPES = {
    'overview': PaperDatabaseEntryOverview,
    'details': PaperDatabaseEntryDetails 
}


def create_db(
    input_file_path: str,
    db_name: str,
    collection_name: str,
    model_name: str,
    n_batches: int,
    data_type) -> None:
    """ Creates a new Mongo database with entries from input_file_path, using model model_name """
    model = load_sentence_transformer(name=model_name)
    df = pd.read_csv(input_file_path)
    df = df.fillna('')
    df_batches = np.array_split(df, n_batches)
    client = MongoClient()
    db = client[db_name]
    col = db[collection_name]
    inserted = 0
    for i, batch in enumerate(df_batches):
        logger.info(f'Processing batch {i}')
        db_entries = []
        for _, row in tqdm(batch.iterrows()):
            db_entry = create_db_entry('data', row, model, data_type)
            # Only add entries with at least one between title and abstract to enable search
            if len(db_entry.title_abstract_embeddings) > 0:
                db_entries.append(db_entry.as_dict())
        col.insert_many(db_entries)
        logger.info(f'Inserted {len(db_entries)} new entries.')
    logger.info(f'Done. {len(df)} processed, {inserted} inserted.')


def update_db(
    old_input_file_path: str,
    input_file_path: str,
    db_name: str,
    collection_name: str,
    model_name: str,
    n_batches: int,
    data_type) -> None:
    """ Updates the DB entries based on old_input_file_path dataframe with new ones based on
    input_file_path, inserting new items and updating the ones that are already present.
    """
    model = load_sentence_transformer(name=model_name)
    df_old = pd.read_csv(old_input_file_path)
    df_old = df_old.fillna('')
    df_new = pd.read_csv(input_file_path)
    df_old = df_old.fillna('')
    if not df_new.equals(df_old):
        modified_new = df_new.merge(
            df_old,
            how='left', 
            indicator=True
        ).loc[lambda f: f['_merge']=='left_only']
        logger.info(f'Total new or updated entries: {len(modified_new)}')
        df_batches = np.array_split(modified_new, n_batches)
        client = MongoClient()
        db = client[db_name]
        col = db[collection_name]
        replaced_count = 0
        for batch in df_batches:
            db_entries = []
            for _, row in tqdm(batch.iterrows()):
                db_entry = create_db_entry('data', row, model, data_type)
                # Only add entries with at least one between title and abstract to enable search
                if len(db_entry.title_abstract_embeddings) > 0:
                    db_entries.append(db_entry.as_dict())
            for entry in db_entries:
                # Replace document if found, else it inserts it
                val = col.find_one_and_replace(
                    {'cord_id': entry['cord_id']},
                    entry,
                    upsert=True
                )
                if val is not None:
                    replaced_count += 1
        inserted_count = len(modified_new) - replaced_count
        logger.info(f'Done: {replaced_count} modified, {inserted_count} new entries.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file_path", 
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
        "--old_input_file_path", 
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
    parser.add_argument(
        "--n_batches", 
        default=1,
        type=int,
        required=False,
        help="The number of batches to use for creating/updating the database."
    )
    parser.add_argument(
        "--collection_type", 
        default="details", 
        type=str, 
        required=False,
        help=f"Specifies collection type in database. One among: {', '.join(TYPES.keys())}"
    )
    args = parser.parse_args()
    if not (args.update != args.create): # XOR
        raise AttributeError('Exactly one among modes "create" and "update" must be selected.')
    if args.update and args.old_input_file_path is None:
        raise AttributeError('The parameter old_input_file_path must be specified when updating.')
    if args.collection_type not in TYPES.keys():
        raise AttributeError(f'Type should be one among: {", ".join(TYPES.keys())}')
    if args.create:
        create_db(
            input_file_path = args.input_file_path,
            db_name = args.db_name,
            collection_name = args.collection_name,
            model_name = args.model_name,
            batches = args.n_batches,
            data_type = TYPES[args.collection_type],
        )
    elif args.update:
        update_db(
            old_input_file_path = args.old_input_file_path,
            input_file_path = args.input_file_path,
            db_name = args.db_name,
            collection_name = args.collection_name,
            model_name = args.model_name,
            batches = args.n_batches,
            data_type = TYPES[args.collection_type],
        )
