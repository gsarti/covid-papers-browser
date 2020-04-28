import argparse
import json
import sys
from tqdm import tqdm

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk


def load_dataset(path, size):
    dataset = []
    with open(path) as f:
        for line in tqdm(f, total=size, desc='Loading JSON'):
            dataset.append(json.loads(line))
    return dataset


def hook(obj):
    value = obj.get("cord_id")
    if value:
        pbar = tqdm(value)
    for item in pbar:
        pass
        pbar.set_description("Loading JSON")
    return obj


def main(args):
    client = Elasticsearch()
    docs = load_dataset(args.data, int(args.size))
    length = len(docs)
    success, failed = 0, 0
    # list of errors to be collected is not stats_only
    errors = []
    stats_only = False
    with tqdm(total=length, desc="Feeding elasticsearch..") as pbar:
        for ok, item in streaming_bulk(client, docs, chunk_size=50):

            # go through request-reponse pairs and detect failures
            if not ok:
                if not stats_only:
                    errors.append(item)
                failed += 1
            else:
                success += 1
            pbar.update(1)
    return success, failed if stats_only else errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing elasticsearch documents.')
    parser.add_argument('--data', required=True, help='Elasticsearch documents.')
    parser.add_argument('--size', required=True, help='Index counter for batch pickles')
    args = parser.parse_args()
    main(args)
