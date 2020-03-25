# CORD19 Data

Place here all the files and folders containing data about Covid-19 and SARS-CoV-v2 articles and papers. Data can be either downloaded from the [Kaggle CORD-19 Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks) or using the following commands:

```shell
DATE=2020-03-20
DATA_DIR=data

wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"${DATE}"/comm_use_subset.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"${DATE}"/noncomm_use_subset.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"${DATE}"/custom_license.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"${DATE}"/biorxiv_medrxiv.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/"${DATE}"/metadata.csv -P "${DATA_DIR}"

tar -zxvf "${DATA_DIR}"/comm_use_subset.tar.gz -C "${DATA_DIR}"
tar -zxvf "${DATA_DIR}"/noncomm_use_subset.tar.gz -C "${DATA_DIR}"
tar -zxvf "${DATA_DIR}"/custom_license.tar.gz -C "${DATA_DIR}"
tar -zxvf "${DATA_DIR}"/biorxiv_medrxiv.tar.gz -C "${DATA_DIR}"
```

As of 20-03-2020, `metadata.csv` has a total of 44220 rows and contains the following information:

- `sha`: Unique identifier, only for files having the full text since it is the hash of the corresponding PDF.

- `source_x`: Article's editor publisher.

- `title`: Title of the paper, not always present.

- `doi`, `pmcid`, `pubmed_id`, `Microsoft Academic Paper ID`, `WHO #Covidence`: Various platform-dependant keys, see `metadata.readme` for more information.

- `license`: The license under which the content is released.

- `abstract`: Abstract of the paper.

- `publish_time`: When the paper was originally published.

- `authors`: Normalized string containing all paper's author names separated by a semicolon.

- `journal`: Venue where the article was originally published.

- `has_full_text`: True if full text is present in one of the folders.

- `full_text_file`: Subfolder in which the full text file is contained, under the name `{sha}.json`.

JSON files inside subfolders are structured as follows:

```python
{
    'paper_id': 'Same as sha in metadata.csv',
    'metadata': {
            'title': 'Title of the paper',
            'authors': [{
                    'first': 'Author firstname',
                    'middle': 'Author middle letter',
                    'last': 'Author lastname',
                    'suffix': 'e.g. Jr.',
                    'affiliation': 'Academic/industrial affiliation',
                    'email': 'Author email'
            }, ...]
    },
    'abstract': [{
            'text': 'Textual content of a part of the section',
            'cite_spans': '?',
            'ref_spans': '?',
            'section': 'Name of the section'
    }]
    'body_text': [{
            'text': 'Textual content of a part of the section',
            'cite_spans': '?',
            'ref_spans': '?',
            'section': 'Name of the section'
    }]
    'bib_entries': {
            'BIBREF0': {
                    'ref_id': 'Reference id',
                    'title': 'Title of the reference',
                    'authors': [{
                            'first': 'Author firstname',
                            'middle': 'Author middle letter',
                            'last': 'Author lastname',
                            'suffix': 'e.g. Jr.'
                    }, ...]
                    'year': 'Year of publication',
                    'venue': 'Venue of publication',
                    'volume': 'Volume of publication',
                    'issn': 'Issue number',
                    'pages': 'Pages in which the publication can be found',
                    'other_ids': 'Dict, all other info on reference'
            }
            'BIBREF1': {
                    ...
            }
            ...
    }
    'ref_entries': {
            'FIGREF0': { # FIGREF, TABREF, etc.
                    'text': 'Reference text description',
                    'latex': 'Latex available for reference',
                    'type': 'table, figure, etc.'
            }
            'TABREF0': {
                    ...
            }
            ...
    }
    'back_matter': [{
            'text': 'Textual content of a part of the section',
            'cite_spans': '?',
            'ref_spans': '?',
            'section': 'Name of the section'
    }]
}
```