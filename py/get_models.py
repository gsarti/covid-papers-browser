from transformers import BertForMaskedLM, TFBertForMaskedLM
import tensorflow as tf
import argparse
import os
import wget
import shutil


def main(args):
    root = os.environ.get('BASE_DIR')
    tmp = root + "/models/tmp/" + args.model
    savepath = root + "/models/" + args.model

    for folder in [tmp,savepath]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # download transformers model and save in tmp folder
    model = BertForMaskedLM.from_pretrained(args.model)
    model.save_pretrained(tmp)

    # Load the PyTorch model in TensorFlow
    tf_model = TFBertForMaskedLM.from_pretrained(tmp, from_pt=True)

    # Save the TensorFlow model
    tf.saved_model.save(tf_model, savepath)

    # Download needed files
    url = "https://s3.amazonaws.com/models.huggingface.co/bert/"+args.model+"/"
    wget.download(url+'config.json', savepath)
    wget.download(url+'vocab.txt', savepath)

    #rename files
    os.rename(savepath+"/config.json",savepath+"/bert_config.json")
    os.rename(savepath+"/variables/variables.data-00000-of-00001", savepath+"/bert_model.ckpt.data-00000-of-00001")
    os.rename(savepath+"/variables/variables.index", savepath+"/bert_model.ckpt.index")

    #remove useless stuff
    os.rmdir(savepath+"/assets")
    os.rmdir(savepath+"/variables")
    os.remove(savepath+"/saved_model.pb")
    shutil.rmtree("./models/tmp")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download transformers models')
    parser.add_argument('--model', required=True, help='model to download.')
    args = parser.parse_args()
    main(args)
