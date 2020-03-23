import os
import argparse
from shutil import rmtree
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import models, SentenceTransformer

MODELS_PATH = "models"

MODELS = ['scibert', 'scibert-nli']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", 
        default="scibert-nli", 
        type=str, 
        required=False,
        help="Model selected in the list: " + ", ".join(MODELS)
    )
    args = parser.parse_args()
    path = os.path.join(MODELS_PATH, args.model)
    if not os.path.exists(path):
        os.makedirs(path)
    if args.model == 'scibert': # Used to fine-tune SciBERT from default embeddings
        tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_cased")
        model = AutoModel.from_pretrained("allenai/scibert_scivocab_cased")
        model.save_pretrained(path)
        tokenizer.save_pretrained(path)
        print('SciBERT Transformer model available in', path)
    elif args.model == 'scibert-nli': # Already-trained SciBERT
        tokenizer = AutoTokenizer.from_pretrained("gsarti/scibert-nli")
        model = AutoModel.from_pretrained("gsarti/scibert-nli")
        model.save_pretrained(path)
        tokenizer.save_pretrained(path)
        word_embedding_model = models.BERT(path)
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                               pooling_mode_mean_tokens=True,
                               pooling_mode_cls_token=False,
                               pooling_mode_max_tokens=False)
        model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
        rmtree(path)
        model.save(path)
        print('SciBERT SentenceTransformer model available in', path)
    else:
        raise AttributeError("Model should be selected in the list: " + ", ".join(MODELS))
