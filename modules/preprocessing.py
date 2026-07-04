"""
=========================================================
PREPROCESSING MODULE
=========================================================
Cleaning
Case Folding
Normalization
Stopword Removal
Stemming
Tokenization
=========================================================
"""

import re
import string
from collections import Counter

import pandas as pd
import streamlit as st

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from config import SLANG_FILE

# =========================================================
# LOAD SLANG DICTIONARY
# =========================================================

@st.cache_resource
def load_slang_dictionary():
    try:
        slang = pd.read_csv(SLANG_FILE)

        slang.columns = [c.lower().strip() for c in slang.columns]

        if "slang" in slang.columns and "formal" in slang.columns:
            return dict(zip(slang["slang"], slang["formal"]))

        return {}

    except Exception:
        return {}


SLANG_DICT = load_slang_dictionary()


# =========================================================
# STOPWORDS
# =========================================================

stop_factory = StopWordRemoverFactory()
STOPWORDS = set(stop_factory.get_stop_words())


# =========================================================
# STEMMER
# =========================================================

stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()

# =========================================================
# VALIDATE TEXT
# =========================================================

def validate_text(text):
    """
    Validasi input text.
    Mengembalikan string kosong jika None/NaN.
    """

    if text is None:
        return ""

    if pd.isna(text):
        return ""

    return str(text).strip()

# =========================================================
# CLEANING
# =========================================================

def cleaning(text):

    text = validate_text(text)

    if text == "":
        return ""

    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"#\w+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"\d+", " ", text)

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# =========================================================
# CASE FOLDING
# =========================================================

def case_folding(text):
    return str(text).lower()


# =========================================================
# NORMALIZATION
# =========================================================

def normalization(text):

    words = text.split()

    words = [
        SLANG_DICT.get(word, word)
        for word in words
    ]

    return " ".join(words)


# =========================================================
# STOPWORD REMOVAL
# =========================================================

def remove_stopword(text):

    if pd.isna(text):
        return ""

    words = text.split()

    words = [
        word
        for word in words
        if word not in STOPWORDS
    ]

    return " ".join(words)


# =========================================================
# STEMMING
# =========================================================

def stemming(text):

    if pd.isna(text):
        return ""

    return stemmer.stem(text)


# =========================================================
# TOKENIZATION
# =========================================================

def tokenization(text):

    if pd.isna(text):
        return []

    return text.split()


# =========================================================
# PREPROCESS SINGLE TEXT
# =========================================================

def preprocess_text(text):
    """
    Preprocess satu review.
    Digunakan oleh:
    - Batch Prediction
    - Single Prediction
    - Dashboard
    """

    original = validate_text(text)

    clean = cleaning(original)
    lower = case_folding(clean)
    normal = normalization(lower)
    stop = remove_stopword(normal)
    stem = stemming(stop)
    token = tokenization(stem)

    return {

        "original_text": original,

        "cleaning": clean,

        "case_folding": lower,

        "normalization": normal,

        "stopword": stop,

        "stemming": stem,

        "token": token,

        "final_text": " ".join(token)

    }
# =========================================================
# PREPROCESS DATAFRAME
# =========================================================

def preprocess_dataframe(df, text_column="review"):
    """
    Preprocess seluruh dataframe.

    Default menggunakan kolom review
    hasil Live Scraper.
    """

    df = df.copy()

    if text_column not in df.columns:
        raise ValueError(
            f"Kolom '{text_column}' tidak ditemukan."
        )

    results = (
        df[text_column]
        .fillna("")
        .apply(preprocess_text)
    )

    df["original_text"] = results.apply(
        lambda x: x["original_text"]
    )

    df["cleaning"] = results.apply(
        lambda x: x["cleaning"]
    )

    df["case_folding"] = results.apply(
        lambda x: x["case_folding"]
    )

    df["normalization"] = results.apply(
        lambda x: x["normalization"]
    )

    df["stopword"] = results.apply(
        lambda x: x["stopword"]
    )

    df["stemming"] = results.apply(
        lambda x: x["stemming"]
    )

    df["token"] = results.apply(
        lambda x: x["token"]
    )

    df["final_text"] = results.apply(
        lambda x: x["final_text"]
    )

    return df
# =========================================================
# PREPROCESSING STATISTICS
# =========================================================

def preprocessing_statistics(df):

    return {
        "Total Review": len(df),
        "Cleaning": df["cleaning"].notna().sum(),
        "Case Folding": df["case_folding"].notna().sum(),
        "Normalization": df["normalization"].notna().sum(),
        "Stopword": df["stopword"].notna().sum(),
        "Stemming": df["stemming"].notna().sum(),
        "Tokenization": df["token"].notna().sum()
    }


# =========================================================
# EMPTY REVIEW
# =========================================================

def empty_review(df):

    return int(
        df["final_text"]
        .fillna("")
        .str.strip()
        .eq("")
        .sum()
    )


# =========================================================
# AVERAGE LENGTH
# =========================================================

def average_length(df):

    if df.empty:
        return 0

    return round(
        df["final_text"]
        .fillna("")
        .apply(lambda x: len(x.split()))
        .mean(),
        2
    )


# =========================================================
# TOP WORDS
# =========================================================

def top_words(df, n=20):

    words = []

    for sentence in df["final_text"].fillna(""):
        words.extend(sentence.split())

    counter = Counter(words)

    return pd.DataFrame(
        counter.most_common(n),
        columns=["Word", "Frequency"]
    )


# =========================================================
# REVIEW LENGTH
# =========================================================

def review_length(df):

    result = df.copy()

    result["review_length"] = (
        result["final_text"]
        .fillna("")
        .apply(lambda x: len(x.split()))
    )

    return result


__all__ = [

    "validate_text",

    "cleaning",

    "case_folding",

    "normalization",

    "remove_stopword",

    "stemming",

    "tokenization",

    "preprocess_text",

    "preprocess_single_review",

    "preprocess_dataframe",

    "preprocessing_statistics",

    "average_length",

    "empty_review",

    "top_words",

    "review_length",

]
]
# =========================================================
# PREPROCESS SINGLE REVIEW
# =========================================================

def preprocess_single_review(text):
    """
    Alias untuk Single Analysis.
    """

    return preprocess_text(text)
