"""
=========================================================
TEXT PREPROCESSING
=========================================================
Cleaning
Case Folding
Normalization
Stopword Removal
Stemming
=========================================================
"""

import re
import string

import pandas as pd

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SLANG_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "slang_dict.json"
)

def replace_slang(text):

    words = text.split()

    words = [
        SLANG_DICT.get(word.lower(), word)
        for word in words
    ]

    return " ".join(words)

with open(SLANG_PATH, "r", encoding="utf-8") as f:
    SLANG_DICT = json.load(f)

from config import *

# ==========================================================
# INITIALIZE
# ==========================================================

stemmer = StemmerFactory().create_stemmer()

stopword = StopWordRemoverFactory().create_stop_word_remover()

# ==========================================================
# CLEANING
# ==========================================================

def cleaning(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # URL
    text = re.sub(r"http\S+|www\S+", " ", text)

    # HTML
    text = re.sub(r"<.*?>", " ", text)

    # Mention
    text = re.sub(r"@\w+", " ", text)

    # Hashtag
    text = re.sub(r"#", " ", text)

    # Angka
    text = re.sub(r"\d+", " ", text)

    # Emoji
    text = re.sub(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        "]+",
        " ",
        text,
        flags=re.UNICODE
    )

    # Tanda baca
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Spasi berlebih
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# ==========================================================
# CASE FOLDING
# ==========================================================

def case_folding(text):

    return text.lower()

# ==========================================================
# NORMALIZATION
# ==========================================================

def normalization(text):

    return replace_slang(text)

# ==========================================================
# STOPWORD
# ==========================================================

def stopword_removal(text):

    return stopword.remove(text)

# ==========================================================
# STEMMING
# ==========================================================

def stemming(text):

    return stemmer.stem(text)

# ==========================================================
# FULL PREPROCESSING
# ==========================================================

def preprocess_text(text):

    text = cleaning(text)

    text = case_folding(text)

    text = normalization(text)

    text = stopword_removal(text)

    text = stemming(text)

    return text

# ==========================================================
# PREPROCESS DATAFRAME
# ==========================================================

def preprocess_dataframe(df, column="review"):

    df = df.copy()

    df["cleaning"] = df[column].apply(cleaning)

    df["case_folding"] = df["cleaning"].apply(case_folding)

    df["normalization"] = df["case_folding"].apply(normalization)

    df["stopword"] = df["normalization"].apply(stopword_removal)

    df["stemming"] = df["stopword"].apply(stemming)

    df["processed_text"] = df["stemming"]

    return df

# ==========================================================
# SINGLE PREPROCESS
# ==========================================================

def preprocess_single(text):

    return preprocess_text(text)

# ==========================================================
# CHECK EMPTY
# ==========================================================

def is_empty(text):

    if text is None:
        return True

    if str(text).strip() == "":
        return True

    return False

# ==========================================================
# WORD COUNT
# ==========================================================

def word_count(text):

    return len(str(text).split())

# ==========================================================
# CHARACTER COUNT
# ==========================================================

def character_count(text):

    return len(str(text))

# ==========================================================
# TOKEN COUNT
# ==========================================================

def token_count(text):

    return len(str(text).split())

# ==========================================================
# TEXT STATISTICS
# ==========================================================

def text_statistics(text):

    return {

        "Characters": character_count(text),

        "Words": word_count(text),

        "Tokens": token_count(text)

    }
