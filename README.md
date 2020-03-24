# Covid-19 Browser: Browse Covid-19 & SARS-CoV-2 Scientific Articles with SciBERT-NLI and BioBERT-NLI 🦠 📖

**Covid-19 Browser** is an interactive experimental tool leveraging a state-of-the-art language model to search relevant content inside the [COVID-19 Open Research Dataset (CORD-19)](https://pages.semanticscholar.org/coronavirus-research) recently published by the White House and its research partners. The dataset contains over 44,000 scholarly articles about COVID-19, SARS-CoV-2 and related coronaviruses.

Various models already fine-tuned on Natural Language Inference are available to perform the search:

- **[`scibert-nli`](https://huggingface.co/gsarti/scibert-nli)**, a fine-tuned version of AllenAI's [SciBERT](https://github.com/allenai/scibert) [1].

- **[`biobert-nli`](https://huggingface.co/gsarti/biobert-nli)**, a fine-tuned version of [BioBERT](https://github.com/dmis-lab/biobert) by J. Lee et al. [2]

Both models are trained on [SNLI](https://nlp.stanford.edu/projects/snli/) [3] and [MultiNLI](https://www.nyu.edu/projects/bowman/multinli/) [4] using the [`sentence-transformers` library](https://github.com/UKPLab/sentence-transformers/) [5] to produce universal sentence embeddings [6]. Embeddings are subsequently used to perform semantic search on CORD-19.

Currently supported operations are:

- Browse paper abstract with interactive queries.

- Reproduce SciBERT-NLI and BioBERT-NLI training results.

## Setup

Python 3.6 or higher is required to run the code. First, install the required libraries with `pip`:

```shell
pip install -r requirements.txt
```

## Using the Browser

First of all, download a model fine-tuned on NLI from HuggingFace's cloud repository.

```shell
python scripts/download_model.py --model scibert-nli
```

Second, download the data from the [Kaggle challenge page](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) and place it in the `data` folder.

Finally, simply run:

```shell
python scripts/interactive_search.py
```

to enter the interactive demo. Using a GPU is suggested since the creation of the embeddings for the entire corpus might be time-consuming otherwise. Both the corpus and the embeddings are cached on disk after the first execution of the script, and execution is really fast after embeddings are computed.

Use the interactive demo as follows:

![Demo GIF](img/demo.gif)

## Reproducing the SciBERT-NLI and BioBERT-NLI Training

First, download SciBERT or BioBERT from HuggingFace's cloud repository.

```shell
python scripts/download_model.py --model scibert
```

Second, download the NLI datasets used for training and the STS dataset used for testing.

```shell
python scripts/get_finetuning_data.py
```

Finally, run the finetuning script by adjusting the parameters depending on the model you intend to train (default is `scibert-nli`).

```shell
python scripts/finetune_nli.py
```

The model will be evaluated against the test portion of the **Semantic Text Similarity (STS)** benchmark dataset at the end of training. Please refer to my [model cards](https://huggingface.co/gsarti) for additional references on parameter values.

## References

[1] Beltagy et al. 2019, ["SciBERT: Pretrained Language Model for Scientific Text"](https://www.aclweb.org/anthology/D19-1371/)

[2] Lee et al. 2020, ["BioBERT: a pre-trained biomedical language representation model for biomedical text mining"](http://doi.org/10.1093/bioinformatics/btz682)

[3] Bowman et al. 2015, ["A large annotated corpus for learning natural language inference"](https://www.aclweb.org/anthology/D15-1075/)

[4] Adina et al. 2018, ["A Broad-Coverage Challenge Corpus for Sentence Understanding through Inference"](http://aclweb.org/anthology/N18-1101)

[5] Reimers et al. 2019, ["Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"](https://www.aclweb.org/anthology/D19-1410/)

[6] As shown in Conneau et al. 2017, ["Supervised Learning of Universal Sentence Representations from Natural Language Inference Data"](https://www.aclweb.org/anthology/D17-1070/)
