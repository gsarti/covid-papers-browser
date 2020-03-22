# Covid-19 Papers Browser

![Demo GIF](img/demo.gif)

Base model: `allenai/scibert-scivocab-cased`
Fine-tuning: AllNLI (Stanford NLI + MultiNLI) for 20000 steps, batch size 64, default script parameters.
Score: 0.745 on STS test set (`bert-base-nli-mean-tokens` achieves 77.12 in ~15000 steps).
