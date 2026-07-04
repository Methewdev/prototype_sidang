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

        slang.columns = [
            c.lower().strip()
            for c in slang.columns
        ]

        if "slang" in slang.columns and "formal" in slang.columns:

            return dict(
                zip(
                    slang["slang"],
                    slang["formal"]
                )
            )

        else:

            return {}

    except Exception:
        # =========================================================
# STOPWORD
# =========================================================

factory = StopWordRemoverFactory()

STOPWORDS = set(
    factory.get_stop_words()
)
# =========================================================
# STEMMER
# =========================================================

factory = StemmerFactory()

stemmer = factory.create_stemmer()
# =========================================================
# CLEANING
# =========================================================

def cleaning(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # URL
    text = re.sub(
        r"http\S+|www\S+",
        " ",
        text
    )

    # Email
    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )

    # Mention
    text = re.sub(
        r"@\w+",
        " ",
        text
    )

    # Hashtag
    text = re.sub(
        r"#\w+",
        " ",
        text
    )

    # HTML
    text = re.sub(
        r"<.*?>",
        " ",
        text
    )

    # Angka
    text = re.sub(
        r"\d+",
        " ",
        text
    )

    # Tanda baca
    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    # Karakter selain huruf
    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )

    # Spasi berlebih
    text = re.sub(
        r"\s+",
        " ",
        text
    )

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

        SLANG_DICT.get(
            word,
            word
        )

        for word in words

    ]

    return " ".join(words)

        return {}

SLANG_DICT = load_slang_dictionary()
# =========================================================
# NORMALIZATION
# =========================================================

def normalization(text):

    words = text.split()

    words = [

        SLANG_DICT.get(
            word,
            word
        )

        for word in words

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

    cleaning_text = cleaning(text)

    case_text = case_folding(cleaning_text)

    normalization_text = normalization(case_text)

    stopword_text = remove_stopword(normalization_text)

    stemming_text = stemming(stopword_text)

    token_text = tokenization(stemming_text)

    final_text = " ".join(token_text)

    return {

        "cleaning": cleaning_text,

        "case_folding": case_text,

        "normalization": normalization_text,

        "stopword": stopword_text,

        "stemming": stemming_text,

        "token": token_text,

        "final_text": final_text

    }
preprocess_dataframe(df, text_column)
# =========================================================
# PREPROCESS DATAFRAME
# =========================================================

def preprocess_dataframe(df, text_column):

    df = df.copy()

    results = df[text_column].apply(preprocess_text)

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
