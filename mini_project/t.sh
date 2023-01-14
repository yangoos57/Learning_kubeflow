#!/bin/bash

torchserve --stop

var="bert_model"

# mar 만들기
torch-model-archiver --model-name ${var} --version 1.0 --serialized-file ./bert_model/pytorch_model.bin  --handler "./torch_serve.py" --extra-files "./bert_model/config.json,./bert_model/vocab.txt"

mv -f ${var}.mar model_store 

# 실행하기
torchserve --start --model-store model_store --models bert=bert_model.mar --no-config-snapshots
