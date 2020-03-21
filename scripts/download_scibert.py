import os
from transformers import AutoTokenizer, AutoModel

SCIBERT_PATH = "models/scibert"

if __name__ == "__main__":
    if not os.path.exists(SCIBERT_PATH):
        os.makedirs(SCIBERT_PATH)
    tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_cased")
    model = AutoModel.from_pretrained("allenai/scibert_scivocab_cased")
    model.save_pretrained(SCIBERT_PATH)
    tokenizer.save_pretrained(SCIBERT_PATH)