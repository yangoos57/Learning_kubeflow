from transformers import DistilBertForTokenClassification, DistilBertTokenizer
from datasets import Dataset
from datasets import Dataset
import pandas as pd

train = pd.read_csv(
    "https://raw.github.com/yangoos57/Learning_kubeflow/main/mini_project/data/train.csv"
)
validation = pd.read_csv(
    "https://raw.github.com/yangoos57/Learning_kubeflow/main/mini_project/data/validation.csv"
)

train_dataset = Dataset.from_pandas(train)
validation_dataset = Dataset.from_pandas(validation)

print("good")

model = DistilBertForTokenClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=len(set(train_dataset["label"]))
)
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")


def tokenize_function(item):
    return tokenizer(item["text"], padding="max_length", max_length=128, truncation=True)


train = train_dataset.map(tokenize_function)
validation = validation_dataset.map(tokenize_function)

print("good2")


from transformers import DistilBertForSequenceClassification, DistilBertTokenizer

model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=len(set(train_dataset["label"]))
)


tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

print("good3")


from transformers import Trainer, TrainingArguments
import os

os.environ["DISABLE_MLFLOW_INTEGRATION"] = "True"


tra_arg = TrainingArguments(
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    eval_steps=10,
    num_train_epochs=1,
    output_dir="test",
    evaluation_strategy="steps",
)


trainer = Trainer(
    model=model,
    args=tra_arg,
    train_dataset=train,
    eval_dataset=validation,
)

trainer.train()

print("good4")


# with open("a11sd.properties", "w") as f:
#     x = dict(
#         inference_address="http://0.0.0.0:8085",
#         management_address="http://0.0.0.0:8085",
#         metrics_address="http://0.0.0.0:8082",
#         grpc_inference_port=7070,
#         grpc_management_port=7071,
#         enable_metrics_api="true",
#         metrics_format="prometheus",
#         number_of_netty_threads=4,
#         job_queue_size=10,
#         enable_envvars_config="true",
#         install_py_dep_per_model="true",
#         model_store="/mnt/models/model-store",
#         model_snapshot={
#             "name": "startup.cfg",
#             "modelCount": 1,
#             "models": {
#                 "mnist": {
#                     "1.0": {
#                         "defaultVersion": "true",
#                         "marName": "mnist.mar",
#                         "minWorkers": 1,
#                         "maxWorkers": 5,
#                         "batchSize": 1,
#                         "maxBatchDelay": 10,
#                         "responseTimeout": 120,
#                     }
#                 }
#             },
#         },
#     )
#     f.write(x)
#     f.close()
