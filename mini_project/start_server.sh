#!/bin/bash

torchserve --stop

model_name="bert-model"

# mar 만들기
torch-model-archiver --model-name ${model_name} --version 1.0 --serialized-file ./bert_model/pytorch_model.bin  --handler "./torch_serve_for_kserve.py" --extra-files "./bert_model/config.json,./bert_model/vocab.txt"

# mv -f ${var}.mar model_store 

# 실행하기
# torchserve --start --model-store model_store --models bert=bert_model.mar --no-config-snapshots --ts-config config.properties