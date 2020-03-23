# Covid-19 Browser: Browse Scientific Covid-19 & SARS-CoV-2 Articles with SciBERT

**Covid-19 Browser** is an interactive experimental tool leveraging a state-of-the-art language model to search relevant content inside the [COVID-19 Open Research Dataset (CORD-19)](https://pages.semanticscholar.org/coronavirus-research) recently published by the White House and its research partners. The dataset contains over 44,000 scholarly articles about COVID-19, SARS-CoV-2 and related coronaviruses.

The model used to perform the search is **[SciBERT-NLI](https://huggingface.co/gsarti/scibert-nli)**, a version of AllenAI's [SciBERT](https://github.com/allenai/scibert) [1] fine tuned on the Natural Language Inference tasks [SNLI](https://nlp.stanford.edu/projects/snli/) [2] and [MultiNLI](https://www.nyu.edu/projects/bowman/multinli/) [3] using the [`sentence-transformers` library](https://github.com/UKPLab/sentence-transformers/) [4] to produce universal sentence embeddings [5]. Embeddings are subsequently used to perform semantic search on CORD-19.

Currently supported operations are:

- Browse paper abstract with interactive queries.

- Reproduce SciBERT-NLI training results.

## Setup

Python 3.6 or higher is required to run the code. First, install the required libraries with `pip`:

```shell
pip install -r requirements.txt
```

## Using the Browser

First of all, download the model from HuggingFace cloud repository.

```shell
python scripts/download_scibert.py
```

Second, download the data from the [Kaggle challenge page](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) and place it in the `data` folder.

Finally, simply run:

```shell
python scripts/interactive_search.py
```

to enter the interactive demo. Using a GPU is suggested since the creation of the embeddings for the entire corpus might be time-consuming otherwise. Both the corpus and the embeddings are cached on disk after the first execution of the script.

Use the interactive demo as follows:

![Demo GIF](img/demo.gif)

## Reproducing the SciBERT-NLI Training

First, download AllenAI SciBERT.

```shell
python scripts/download_scibert.py --model scibert
```

Second, download the NLI datasets used for training and the STS dataset used for testing.

```shell
python scripts/get_finetuning_data.py
```

Finally, run the finetuning script. 

```shell
python scripts/finetune_nli.py
```

The model will be evaluated against the test portion of the Semantic Text Similarity (STS) benchmark dataset at the end of training. Default parameters were the ones used for training `gsarti/scibert-nli`.

## References

[1] Beltagy et al. 2019, ["SciBERT: Pretrained Language Model for Scientific Text"](https://www.aclweb.org/anthology/D19-1371/)

[2] Bowman et al. 2015, ["A large annotated corpus for learning natural language inference"](https://www.aclweb.org/anthology/D15-1075/)

[3] Adina et al. 2018, ["A Broad-Coverage Challenge Corpus for Sentence Understanding through Inference"](http://aclweb.org/anthology/N18-1101)

[4] Reimers et al. 2019, ["Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"](https://www.aclweb.org/anthology/D19-1410/)

[5] As shown in Conneau et al. 2017, ["Supervised Learning of Universal Sentence Representations from Natural Language Inference Data"](https://www.aclweb.org/anthology/D17-1070/)
