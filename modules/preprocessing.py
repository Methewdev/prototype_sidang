"""
=========================================================
PREPROCESSING MODULE
=========================================================

Pipeline:

1. Cleaning
2. Case Folding
3. Normalization
4. Tokenization

Catatan:
- Stopword Removal tidak digunakan
- Stemming tidak digunakan
- Emoji dipertahankan
- Repeated character handling dilakukan pada tahap Normalization
- Tokenisasi final model dilakukan menggunakan tokenizer Transformer
=========================================================
"""

import re
import string
from collections import Counter

import pandas as pd
import streamlit as st

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

            slang["slang"] = (
                slang["slang"]
                .astype(str)
                .str.lower()
                .str.strip()
            )

            slang["formal"] = (
                slang["formal"]
                .astype(str)
                .str.lower()
                .str.strip()
            )

            return dict(
                zip(
                    slang["slang"],
                    slang["formal"]
                )
            )

        return {}

    except Exception:

        return {}


SLANG_DICT = load_slang_dictionary()


# =========================================================
# SLANG TAMBAHAN
# =========================================================

COMMON_SLANG = {

    "gw": "saya",
    "gua": "saya",
    "gue": "saya",

    "lu": "kamu",
    "loe": "kamu",

    "udah": "sudah",
    "udh": "sudah",
    "dah": "sudah",

    "gak": "tidak",
    "ga": "tidak",
    "gk": "tidak",
    "nggak": "tidak",
    "ngga": "tidak",
    "enggak": "tidak",

    "gajelas": "tidak jelas",

    "bgt": "banget",

    "yg": "yang",
    "dgn": "dengan",
    "dr": "dari",
    "utk": "untuk",

    "krn": "karena",
    "karna": "karena",

    "tp": "tapi",
    "tpi": "tapi",

    "blm": "belum",
    "belom": "belum",

    "bkn": "bukan",

    "sm": "sama",
    "sma": "sama",

    "aja": "saja",
    "aj": "saja",

    "kalo": "kalau",
    "kl": "kalau",

    "makasih": "terima kasih",
    "mksh": "terima kasih",
    "thx": "terima kasih",

    "pls": "tolong",
    "plis": "tolong",

    "dpt": "dapat",
    "dapet": "dapat",

    "pake": "pakai",

    "bikin": "membuat",

    "mantul": "mantap"
}


SLANG_DICT = {
    **COMMON_SLANG,
    **SLANG_DICT
}


# =========================================================
# VALIDATE TEXT
# =========================================================

def validate_text(text):

    if text is None:
        return ""

    try:

        if pd.isna(text):
            return ""

    except Exception:

        pass

    return str(text).strip()


# =========================================================
# 4.3.1 CLEANING
# =========================================================

def cleaning(text):

    text = validate_text(text)

    if text == "":
        return ""

    # URL
    text = re.sub(
        r"https?://\S+|www\.\S+",
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
    # simbol # dihapus,
    # tetapi isi kata tetap dipertahankan
    text = re.sub(
        r"#",
        "",
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

    # Punctuation
    # Emoji TIDAK dihapus
    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    # Spasi berlebih
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# 4.3.2 CASE FOLDING
# =========================================================

def case_folding(text):

    text = validate_text(text)

    return text.lower()


# =========================================================
# 4.3.3 NORMALIZATION
# =========================================================

def normalization(text):

    text = validate_text(text)

    if text == "":
        return ""

    # -----------------------------------------------------
    # Normalisasi karakter berulang
    #
    # baguuuus -> bagus
    # lamaaaaa -> lama
    # mantaaap -> mantap
    # -----------------------------------------------------

    text = re.sub(
        r"(.)\1{2,}",
        r"\1",
        text
    )

    # -----------------------------------------------------
    # Normalisasi slang
    # -----------------------------------------------------

    words = text.split()

    normalized_words = []

    for word in words:

        replacement = SLANG_DICT.get(
            word,
            word
        )

        normalized_words.append(
            replacement
        )

    return " ".join(
        normalized_words
    )


# =========================================================
# 4.3.4 TOKENIZATION
# =========================================================

def tokenization(text):

    text = validate_text(text)

    if text == "":
        return []

    return text.split()


# =========================================================
# PREPROCESS SINGLE TEXT
# =========================================================

def preprocess_text(text):

    original = validate_text(text)

    clean = cleaning(
        original
    )

    lower = case_folding(
        clean
    )

    normal = normalization(
        lower
    )

    token = tokenization(
        normal
    )

    return {

        "original_text":
            original,

        "cleaning":
            clean,

        "case_folding":
            lower,

        "normalization":
            normal,

        "token":
            token,

        "final_text":
            normal

    }


# =========================================================
# PREPROCESS DATAFRAME
# =========================================================

def preprocess_dataframe(
    df,
    text_column="review"
):

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
        lambda x:
        x["original_text"]
    )

    df["cleaning"] = results.apply(
        lambda x:
        x["cleaning"]
    )

    df["case_folding"] = results.apply(
        lambda x:
        x["case_folding"]
    )

    df["normalization"] = results.apply(
        lambda x:
        x["normalization"]
    )

    df["token"] = results.apply(
        lambda x:
        x["token"]
    )

    df["final_text"] = results.apply(
        lambda x:
        x["final_text"]
    )

    return df


# =========================================================
# STATISTICS
# =========================================================

def preprocessing_statistics(df):

    return {

        "Total Review":
            len(df),

        "Cleaning":
            df["cleaning"].notna().sum(),

        "Case Folding":
            df["case_folding"].notna().sum(),

        "Normalization":
            df["normalization"].notna().sum(),

        "Tokenization":
            df["token"].notna().sum()

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
        .apply(
            lambda x:
            len(x.split())
        )
        .mean(),

        2
    )


# =========================================================
# TOP WORDS
# =========================================================

def top_words(
    df,
    n=20
):

    words = []

    for sentence in (
        df["final_text"]
        .fillna("")
    ):

        words.extend(
            sentence.split()
        )

    counter = Counter(words)

    return pd.DataFrame(

        counter.most_common(n),

        columns=[
            "Word",
            "Frequency"
        ]

    )


# =========================================================
# REVIEW LENGTH
# =========================================================

def review_length(df):

    result = df.copy()

    result["review_length"] = (

        result["final_text"]
        .fillna("")
        .apply(
            lambda x:
            len(x.split())
        )

    )

    return result


# =========================================================
# SINGLE REVIEW
# =========================================================

def preprocess_single_review(text):

    return preprocess_text(text)


# =========================================================
# EXPORT
# =========================================================

__all__ = [

    "validate_text",

    "cleaning",

    "case_folding",

    "normalization",

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
