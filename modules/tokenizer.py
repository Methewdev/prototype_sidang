"""
=========================================================
TOKENIZER MODULE
=========================================================
IndoBERT Tokenizer
=========================================================
"""

import pandas as pd
from transformers import AutoTokenizer

from config import HF_MODEL, MAX_LENGTH

# ==========================================================
# LOAD TOKENIZER
# ==========================================================

tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)

# ==========================================================
# TOKENIZE SINGLE TEXT
# ==========================================================

def tokenize_text(text):

    encoding = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
        return_tensors=None
    )

    tokens = tokenizer.convert_ids_to_tokens(
        encoding["input_ids"]
    )

    return {
        "tokens": tokens,
        "input_ids": encoding["input_ids"],
        "attention_mask": encoding["attention_mask"]
    }

# ==========================================================
# TOKEN COUNT
# ==========================================================

def count_tokens(text):

    result = tokenize_text(text)

    tokens = result["tokens"]

    return len(tokens)

# ==========================================================
# TOKEN TABLE
# ==========================================================

def token_dataframe(text):

    result = tokenize_text(text)

    df = pd.DataFrame({

        "Token": result["tokens"],

        "Input ID": result["input_ids"],

        "Attention Mask": result["attention_mask"]

    })

    return df

# ==========================================================
# DECODE TOKEN
# ==========================================================

def decode_ids(input_ids):

    return tokenizer.decode(
        input_ids,
        skip_special_tokens=False
    )

# ==========================================================
# SPECIAL TOKEN
# ==========================================================

def special_tokens():

    return {

        "CLS": tokenizer.cls_token,

        "SEP": tokenizer.sep_token,

        "PAD": tokenizer.pad_token,

        "UNK": tokenizer.unk_token,

        "MASK": tokenizer.mask_token

    }

# ==========================================================
# VOCAB SIZE
# ==========================================================

def vocabulary_size():

    return tokenizer.vocab_size

# ==========================================================
# MAX LENGTH
# ==========================================================

def max_length():

    return tokenizer.model_max_length

# ==========================================================
# TOKENIZER INFO
# ==========================================================

def tokenizer_information():

    return {

        "Tokenizer": HF_MODEL,

        "Vocabulary Size": vocabulary_size(),

        "Maximum Length": max_length(),

        "CLS Token": tokenizer.cls_token,

        "SEP Token": tokenizer.sep_token,

        "PAD Token": tokenizer.pad_token

    }

# ==========================================================
# DATAFRAME TOKENIZER
# ==========================================================

def tokenize_dataframe(df, column="processed_text"):

    df = df.copy()

    token_length = []

    input_ids = []

    attention_masks = []

    tokens = []

    for text in df[column]:

        result = tokenize_text(str(text))

        token_length.append(

            len(result["tokens"])

        )

        input_ids.append(

            result["input_ids"]

        )

        attention_masks.append(

            result["attention_mask"]

        )

        tokens.append(

            result["tokens"]

        )

    df["token_count"] = token_length

    df["tokens"] = tokens

    df["input_ids"] = input_ids

    df["attention_mask"] = attention_masks

    return df

# ==========================================================
# PREVIEW
# ==========================================================

def preview_token(text):

    result = tokenize_text(text)

    print("="*60)

    print("Original Text")

    print(text)

    print()

    print("="*60)

    print("Tokens")

    print(result["tokens"])

    print()

    print("="*60)

    print("Input IDs")

    print(result["input_ids"])

    print()

    print("="*60)

    print("Attention Mask")

    print(result["attention_mask"])

    print("="*60)
