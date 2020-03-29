# CORD19 Data

Place here all the files and folders containing data about Covid-19 and SARS-CoV-v2 articles and papers. Data can be either downloaded from the [Kaggle CORD-19 Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks) or by calling the script `download_data.sh`.

As of 29-03-2020, `metadata.csv` has a total of 45774 rows and contains the following information:

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

JSON files inside subfolders are divided as:

- `biorxiv_medrxiv`: 1053 full text

- `comm_use_subset`: 9315 full text

- `custom_license`: 20657 full text

- `noncomm_use_subset`: 2350 full text

and are structured as follows:

```python
{
    "paper_id": <str>,                      # 40-character sha1 of the PDF
    "metadata": {
        "title": <str>,
        "authors": [                        # list of author dicts, in order
            {
                "first": <str>,
                "middle": <list of str>,
                "last": <str>,
                "suffix": <str>,
                "affiliation": <dict>,
                "email": <str>
            },
            ...
        ],
        "abstract": [                       # list of paragraphs in the abstract
            {
                "text": <str>,
                "cite_spans": [             # list of character indices of inline citations
                                            # e.g. citation "[7]" occurs at positions 151-154 in "text"
                                            #      linked to bibliography entry BIBREF3
                    {
                        "start": 151,
                        "end": 154,
                        "text": "[7]",
                        "ref_id": "BIBREF3"
                    },
                    ...
                ],
                "ref_spans": <list of dicts similar to cite_spans>,     # e.g. inline reference to "Table 1"
                "section": "Abstract"
            },
            ...
        ],
        "body_text": [                      # list of paragraphs in full body
                                            # paragraph dicts look the same as above
            {
                "text": <str>,
                "cite_spans": [],
                "ref_spans": [],
                "eq_spans": [],
                "section": "Introduction"
            },
            ...
            {
                ...,
                "section": "Conclusion"
            }
        ],
        "bib_entries": {
            "BIBREF0": {
                "ref_id": <str>,
                "title": <str>,
                "authors": <list of dict>       # same structure as earlier,
                                                # but without `affiliation` or `email`
                "year": <int>,
                "venue": <str>,
                "volume": <str>,
                "issn": <str>,
                "pages": <str>,
                "other_ids": {
                    "DOI": [
                        <str>
                    ]
                }
            },
            "BIBREF1": {},
            ...
            "BIBREF25": {}
        },
        "ref_entries":
            "FIGREF0": {
                "text": <str>,                  # figure caption text
                "type": "figure"
            },
            ...
            "TABREF13": {
                "text": <str>,                  # table caption text
                "type": "table"
            }
        },
        "back_matter": <list of dict>           # same structure as body_text
    }
}
```
