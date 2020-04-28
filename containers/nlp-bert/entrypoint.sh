#!/bin/sh



bert-serving-start -num_worker 4 -max_seq_len 128  -model_dir /model -http_port 8001
