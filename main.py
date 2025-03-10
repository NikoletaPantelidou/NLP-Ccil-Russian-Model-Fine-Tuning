# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 20:00:05 2025

@author: nikol
"""

#----------------------------DEFINE THE MODEL-------------------------------------------------------#
# Load the model from Hugging Face
from transformers import AutoTokenizer, AutoModelForTokenClassification

tokenizer = AutoTokenizer.from_pretrained("viktoroo/sberbank-rubert-base-collection3")
model = AutoModelForTokenClassification.from_pretrained("viktoroo/sberbank-rubert-base-collection3")


#----------------------------DEFINE THE DATASET-----------------------------------------------------#




#---------------------------FINE-TUNE THE MODEL-----------------------------------------------------#

def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)

    labels = []
    for i, label in enumerate(examples[f"ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:  # Set the special tokens to -100.
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:  # Only label the first token of a given word.
                label_ids.append(label[word_idx])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs