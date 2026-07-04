"""
=========================================================
PREPROCESSING MODULE
Livin Emotion Analysis
=========================================================
"""

import re
import pandas as pd

from config import SLANG_FILE

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import (
    StopWordRemoverFactory
)

# =====================================================
# INITIALIZE
# =====================================================

stemmer = StemmerFactory().create_stemmer()

stopword = StopWordRemoverFactory().create_stop_word_remover()

# =====================================================
# LOAD SLANG DICTIONARY
# =====================================================

def load_slang_dictionary():

    if not SLANG_FILE.exists():

        raise FileNotFoundError(
            f"File slang tidak ditemukan:\n{SLANG_FILE}"
        )

    # membaca file dari GitHub new_kamus_alay.csv
    slang_df = pd.read_csv(
        SLANG_FILE,
        header=None,
        names=["slang", "formal"],
        encoding="utf-8"
    )

    slang_df = slang_df.dropna()

    slang_df["slang"] = slang_df["slang"].astype(str).str.strip()

    slang_df["formal"] = slang_df["formal"].astype(str).str.strip()

    slang_dict = dict(
        zip(
            slang_df["slang"],
            slang_df["formal"]
        )
    )

    return slang_dict


SLANG_DICT = load_slang_dictionary()

# =====================================================
# CLEANING
# =====================================================

def cleaning(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # URL
    text = re.sub(r"http\S+", " ", text)

    # WWW
    text = re.sub(r"www\S+", " ", text)

    # Mention
    text = re.sub(r"@\w+", " ", text)

    # Hashtag
    text = re.sub(r"#\w+", " ", text)

    # Angka
    text = re.sub(r"\d+", " ", text)

    # Emoji
    text = re.sub(r"[^\w\s]", " ", text)

    # Multiple Space
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# CASE FOLDING
# =====================================================

def case_folding(text):

    if pd.isna(text):
        return ""

    return str(text).lower()


# =====================================================
# NORMALIZATION
# =====================================================

def normalization(text):

    if pd.isna(text):
        return ""

    words = str(text).split()

    normalized = []

    for word in words:

        normalized.append(

            SLANG_DICT.get(

                word,

                word

            )

        )

    return " ".join(normalized)


# =====================================================
# STOPWORD REMOVAL
# =====================================================

def stopword_removal(text):

    if pd.isna(text):
        return ""

    return stopword.remove(str(text))


# =====================================================
# STEMMING
# =====================================================

def stemming(text):

    if pd.isna(text):
        return ""

    return stemmer.stem(str(text))


# =====================================================
# TOKENIZATION
# =====================================================

def tokenization(text):

    if pd.isna(text):
        return ""

    tokens = str(text).split()

    return " | ".join(tokens)


# =====================================================
# PREPROCESS SINGLE TEXT
# =====================================================

def preprocess_text(text):

    clean = cleaning(text)

    lower = case_folding(clean)

    normal = normalization(lower)

    stop = stopword_removal(normal)

    stem = stemming(stop)

    token = tokenization(stem)

    return {

        "cleaning": clean,

        "case_folding": lower,

        "normalization": normal,

        "stopword": stop,

        "stemming": stem,

        "token": token,

        "final_text": stem

    }


# =====================================================
# PREPROCESS DATAFRAME
# =====================================================

def preprocess_dataframe(df, text_column):

    data = df.copy()

    result = data[text_column].apply(preprocess_text)

    result = pd.DataFrame(result.tolist())

    data = pd.concat(

        [

            data,

            result

        ],

        axis=1

    )

    return data


# =====================================================
# PREVIEW
# =====================================================

def preview_preprocessing(df, n=10):

    columns = [

        "cleaning",

        "case_folding",

        "normalization",

        "stopword",

        "stemming",

        "token"

    ]

    return df[columns].head(n)


# =====================================================
# PREPROCESS STATISTIC
# =====================================================

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
