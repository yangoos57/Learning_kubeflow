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
