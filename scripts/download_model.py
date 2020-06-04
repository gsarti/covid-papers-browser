import os
import argparse
from shutil import rmtree
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import models, SentenceTransformer

MODELS_PATH = "models"

MODELS_PRETRAINED = {
    'scibert': 'allenai/scibert_scivocab_cased',
    'biobert': 'monologg/biobert_v1.1_pubmed',
    'covidbert': ' deepset/covid_bert_base',
    'clinicalcovidbert': 'manueltonneau/clinicalcovid-bert-base-cased',
    'biocovidbert': 'manueltonneau/biocovid-bert-large-cased'}

MODELS_FINETUNED = {
    'scibert-nli': 'gsarti/scibert-nli',
    'biobert-nli': 'gsarti/biobert-nli',
    'covidbert-nli': 'gsarti/covidbert-nli',
    'clinicalcovidbert-nli':'manueltonneau/clinicalcovid-bert-nli'
}

MODELS = {**MODELS_PRETRAINED, **MODELS_FINETUNED}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", 
        default="scibert-nli", 
        type=str, 
        required=False,
        help="Model selected in the list: " + 
             ", ".join(list(MODELS_PRETRAINED) + list(MODELS_FINETUNED))
    )
    parser.add_argument(
        "--do_lower_case", 
        action="store_true",
        help="Use a cased language model."
    )
    parser.add_argument(
        "--max_seq_length", 
        default=128, 
        type=int,
        required=False,
        help="Sequence length used by the language model."
    )
    parser.add_argument(
        "--output_dir",  
        type=str,
        help="Directory where the models are saved."
    )    
    args = parser.parse_args()
    path = os.path.join(args.output_dir, MODELS_PATH, args.model)
    if not os.path.exists(path):
        os.makedirs(path)
    if args.model not in list(MODELS_PRETRAINED) + list(MODELS_FINETUNED):
        raise AttributeError("Model should be selected in the list: " + 
            ", ".join(list(MODELS_PRETRAINED) + list(MODELS_FINETUNED))
        )
    tokenizer = AutoTokenizer.from_pretrained(MODELS[args.model])
    model = AutoModel.from_pretrained(MODELS[args.model])
    model.save_pretrained(path)
    tokenizer.save_pretrained(path)
    if args.model in MODELS_FINETUNED.keys(): # Build the SentenceTransformer directly
        word_embedding_model = models.BERT(
            path,
            max_seq_length=args.max_seq_length,
            do_lower_case=args.do_lower_case
        )
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                               pooling_mode_mean_tokens=True,
                               pooling_mode_cls_token=False,
                               pooling_mode_max_tokens=False)
        model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
        rmtree(path)
        model.save(path)
    print(f'Model {args.model} available in', path)
