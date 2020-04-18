""" Classes used as returns for API methods """

import numpy as np

class PaperDatabaseEntryOverview:
    """ Defines the PaperDatabaseEntryOverview object stored in the database used to retrieve the list of papers. """
    def __init__(self, x):
        self.cord_id = x['cord_uid']
        self.title = x['title'] if x['title'] not in FILTER_TITLES else ''
        self.license = x['license']
        self.abstract = x['abstract'] if x['abstract'] not in FILTER_ABSTRACTS else ''
        self.publish_time = x['publish_time']
        self.authors = x['authors'].split('; ')
        self.journal = x['journal']
        self.title_abstract_embeddings = []

    def as_dict(self):
        return {
            'cord_id': self.cord_id,
            'title': self.title,
            'license': self.license,
            'abstract': self.abstract,
            'publish_time': self.publish_time,
            'authors': self.authors,
            'journal': self.journal,
            'title_abstract_embeddings': self.title_abstract_embeddings,
        }

    def compute_title_abstract_embeddings(self, model):
        # We compute embeddings only for papers with abstracts available.
        if self.abstract != '':
            title_abstract = self.title + ' ' + self.abstract
            embedding = model.encode([title_abstract], show_progress_bar=False)
            self.title_abstract_embeddings = embedding[0].tolist()


class PaperDatabaseEntryDetails(PaperDatabaseEntryOverview):
    """ Defines the PaperDatabaseEntryDetails object stored in the database containing additional information for single-paper view. """
    def __init__(self, x):
        super().__init__(x)
        self.url = x['url']
        self.sha = x['sha'].split(';')[0]
        self.source = x['source_x']
        self.doi = x['doi']
        self.pmc_id = x['pmcid']
        self.pubmed_id = x['pubmed_id']
        self.microsoft_id = x['Microsoft Academic Paper ID']
        self.who_id = x['WHO #Covidence']
        self.paragraphs = [] # List of tuples (section_name, text)
        self.bibliography = [] # List of dictionaries
        self.paragraphs_embeddings = []

    def as_dict(self):
        return {
            'cord_id': self.cord_id,
            'url': self.url,
            'sha': self.sha,
            'title': self.title,
            'source': self.source,
            'doi': self.doi,
            'pmc_id': self.pmc_id,
            'pubmed_id': self.pubmed_id,
            'license': self.license,
            'abstract': self.abstract,
            'publish_time': self.publish_time,
            'authors': self.authors,
            'journal': self.journal,
            'microsoft_id': self.microsoft_id,
            'who_id': self.who_id,
            'paragraphs': self.paragraphs,
            'bibliography': self.bibliography,
            'title_abstract_embeddings': self.title_abstract_embeddings,
            'paragraphs_embeddings': self.paragraphs_embeddings,
        }
    
    def compute_paragraphs_embeddings(self, model):
        if len(self.paragraphs) > 0:
            paragraphs_text = [tup[1] for tup in self.paragraphs]
            paragraph_embeddings = model.encode(paragraphs_text, show_progress_bar=False)
            self.paragraphs_embeddings = [e.tolist() for e in paragraph_embeddings]
    

class PaperOverview:
    """ Defines the PaperOverview object returned to the views in dict format. """
    def __init__(self, dic):
        self.cord_id = dic['cord_id']
        self.title = dic['title']
        self.journal = dic['journal']
        self.authors = dic['authors']
        self.abstract = dic['abstract']
        self.license = dic['license']
        self.year = dic['publish_time'].split('-')[0]

    def as_dict(self, score=-1):
        return {
            'cord_id': self.cord_id,
            'title': self.title,
            'abstract': self.abstract,
            'authors': ", ".join(self.authors),
            'journal': self.journal,
            'year': self.year,
            'score': round(score, 2)
        }


class PaperDetails(PaperOverview):
    """ Defines the Paper object used when querying a single DB item """
    def __init__(self, dic):
        super().__init__(dic)
        self.url = dic['url']
        self.source = dic['source']
        self.doin = dic['doi']
        self.pmc_id = dic['pmc_id']
        self.pubmed_id = dic['pubmed_id']
        self.license = dic['license']
        self.publish_time = dic['publish_time']
        self.microsoft_id = dic['microsoft_id']
        self.who_id = dic['who_id']
        self.paragraphs = dic['paragraphs'] # List of tuples (section_name, text)
        self.ranked_paragraphs = []
        self.bibliography = dic['bibliography'] # List of dictionaries
        self.paragraphs_embeddings = [np.array(e) for e in dic['paragraphs_embeddings']]

    def as_dict(self, scores=[], indices=[]):
        return {
            'cord_id': self.cord_id,
            'title': self.title,
            'abstract': self.abstract,
            'authors': self.authors,
            'journal': self.journal,
            'url': self.url,
            'source': self.source,
            'doin': self.doin,
            'pmc_id': self.pmc_id,
            'pubmed_id': self.pubmed_id,
            'license': self.license,
            'publish_time': self.publish_time,
            'microsoft_id': self.microsoft_id,
            'who_id': self.who_id,
            'ranked_paragraphs': [{
                'section': p[0],
                'text': p[1],
                'score': round(scores[i], 2) if len(scores) > 0 else -1.0,
                'spans': indices[i] if len(indices) > 0 else []
            } for i, p in enumerate(self.ranked_paragraphs)],
            'bibliography': self.bibliography,
        }



# Most frequent titles that should be treated as missing
FILTER_TITLES = ['Index', 'Subject Index', 'Subject index', 'Author index', 'Contents', 
    'Articles of Significant Interest Selected from This Issue by the Editors',
    'Information for Authors', 'Graphical contents list', 'Table of Contents',
    'In brief', 'Preface', 'Editorial Board', 'Author Index', 'Volume Contents',
    'Research brief', 'Abstracts', 'Keyword index', 'In This Issue', 'Department of Error',
    'Contents list', 'Highlights of this issue', 'Abbreviations', 'Introduction',
    'Cumulative Index', 'Positions available', 'Index of Authors', 'Editorial',
    'Journal Watch', 'QUIZ CORNER', 'Foreword', 'Table of contents', 'Quiz Corner',
    'INDEX', 'Bibliography of the current world literature', 'Index of Subjects',
    '60 Seconds', 'Contributors', 'Public Health Watch', 'Commentary',
    'Chapter 1 Introduction', 'Facts and ideas from anywhere', 'Erratum',
    'Contents of Volume', 'Patent reports', 'Oral presentations', 'Abkürzungen',
    'Abstracts cont.', 'Related elsevier virology titles contents alert', 'Keyword Index',
    'Volume contents', 'Articles of Significant Interest in This Issue', 'Appendix', 
    'Abkürzungsverzeichnis', 'List of Abbreviations', 'Editorial Board and Contents',
    'Instructions for Authors', 'Corrections', 'II. Sachverzeichnis', '1 Introduction',
    'List of abbreviations', 'Response', 'Feedback', 'Poster Sessions', 'News Briefs',
    'Commentary on the Feature Article', 'Papers to Appear in Forthcoming Issues', 'TOC',
    'Glossary', 'Letter from the editor', 'Croup', 'Acronyms and Abbreviations',
    'Highlights', 'Forthcoming papers', 'Poster presentations', 'Authors',
    'Journal Roundup', 'Index of authors', 'Table des mots-clés', 'Posters',
    'Cumulative Index 2004', 'A Message from the Editor', 'Contents and Editorial Board',
    'SUBJECT INDEX', 'Contents page 1',
]

# Abstracts that should be treated as missing abstract
FILTER_ABSTRACTS = ['Unknown', '[Image: see text]']