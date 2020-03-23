
"""
Adapted from the original sentence-transformers script:

https://github.com/UKPLab/sentence-transformers/blob/master/examples/datasets/get_data.py
"""

import urllib.request
import zipfile
import os

folder_path = 'data'
print('Beginning download of datasets')

datasets = ['AllNLI.zip', 'stsbenchmark.zip']
server = "https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/datasets/"

if not os.path.exists(folder_path):
    os.mkdir(folder_path)

for dataset in datasets:
    print("Download", dataset)
    url = server+dataset
    dataset_path = os.path.join(folder_path, dataset)
    urllib.request.urlretrieve(url, dataset_path)

    print("Extract", dataset)
    with zipfile.ZipFile(dataset_path, "r") as zip_ref:
        zip_ref.extractall(folder_path)
    os.remove(dataset_path)

print("All datasets downloaded and extracted")