"""
=========================================================
PREPROCESSING MODULE
=========================================================
Pipeline:

1. Cleaning
2. Case Folding
3. Normalization
4. Repeated Character Handling
5. Tokenization

Catatan:
- Stopword Removal TIDAK digunakan
- Stemming TIDAK digunakan
- Emoji dipertahankan karena dapat menjadi sinyal emosi
- Pipeline disesuaikan untuk model Transformer/BERT
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
# TAMBAHAN SLANG UMUM
# =========================================================
# Digunakan untuk memastikan beberapa contoh pada tesis
# seperti:
# gw -> saya
# udah -> sudah
# gajelas -> tidak jelas
# gak -> tidak
# dll.
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
    "ga jelas": "tidak jelas",

    "bgt": "banget",
    "banget": "banget",

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
    "pakai": "pakai",

    "bikin": "membuat",
    "bgt": "banget",

    "mantul": "mantap",

}


# Gabungkan dictionary eksternal + dictionary tambahan

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
# CLEANING
# =========================================================

def cleaning(text):

    text = validate_text(text)

    if text == "":
        return ""

    # -----------------------------------------------------
    # URL
    # -----------------------------------------------------

    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # -----------------------------------------------------
    # EMAIL
    # -----------------------------------------------------

    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )

    # -----------------------------------------------------
    # USERNAME / MENTION
    # -----------------------------------------------------

    text = re.sub(
        r"@\w+",
        " ",
        text
    )

    # -----------------------------------------------------
    # HASHTAG
    # -----------------------------------------------------

    # #
    # dihapus tetapi kata setelahnya dipertahankan
    #
    # contoh:
    # #LivinMandiri
    # menjadi:
    # LivinMandiri
    # -----------------------------------------------------

    text = re.sub(
        r"#",
        "",
        text
    )

    # -----------------------------------------------------
    # HTML
    # -----------------------------------------------------

    text = re.sub(
        r"<.*?>",
        " ",
        text
    )

    # -----------------------------------------------------
    # ANGKA
    # -----------------------------------------------------

    text = re.sub(
        r"\d+",
        " ",
        text
    )

    # -----------------------------------------------------
    # PUNCTUATION
    # -----------------------------------------------------

    # Emoji TIDAK dihapus.
    #
    # Kita hanya menghapus punctuation ASCII.
    #
    # Contoh:
    # ! ? , . tetap dibersihkan
    # 😡 😭 😍 ❤️ tetap dipertahankan
    # -----------------------------------------------------

    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    # -----------------------------------------------------
    # NORMALISASI SPASI
    # -----------------------------------------------------

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

    text = validate_text(text)

    return text.lower()


# =========================================================
# NORMALIZATION
# =========================================================

def normalization(text):

    text = validate_text(text)

    if text == "":
        return ""

    words = text.split()

    normalized_words = []

    for word in words:

        # Cari langsung di dictionary
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
# REPEATED CHARACTER HANDLING
# =========================================================

def repeated_character_handling(text):

    text = validate_text(text)

    if text == "":
        return ""

    # -----------------------------------------------------
    # Mengurangi karakter berulang:
    #
    # baguuuus -> bagus
    # lamaaaaa -> lama
    # mantaaap -> mantap
    #
    # Maksimal dua karakter berturut-turut.
    # -----------------------------------------------------

    text = re.sub(
        r"(.)\1{2,}",
        r"\1",
        text
    )

    return text


# =========================================================
# TOKENIZATION
# =========================================================

def tokenization(text):

    text = validate_text(text)

    if text == "":
        return []

    # Tokenisasi sederhana untuk tampilan.
    #
    # Tokenisasi utama saat masuk model tetap
    # menggunakan tokenizer IndoBERT.
    #

    return text.split()


# =========================================================
# PREPROCESS SINGLE TEXT
# =========================================================

def preprocess_text(text):

    original = validate_text(
        text
    )

    clean = cleaning(
        original
    )

    lower = case_folding(
        clean
    )

    normal = normalization(
        lower
    )

    repeated = repeated_character_handling(
        normal
    )

    token = tokenization(
        repeated
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

        "repeated_character":
            repeated,

        "token":
            token,

        "final_text":
            repeated

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

    # -----------------------------------------------------
    # ORIGINAL
    # -----------------------------------------------------

    df["original_text"] = results.apply(
        lambda x:
        x["original_text"]
    )

    # -----------------------------------------------------
    # CLEANING
    # -----------------------------------------------------

    df["cleaning"] = results.apply(
        lambda x:
        x["cleaning"]
    )

    # -----------------------------------------------------
    # CASE FOLDING
    # -----------------------------------------------------

    df["case_folding"] = results.apply(
        lambda x:
        x["case_folding"]
    )

    # -----------------------------------------------------
    # NORMALIZATION
    # -----------------------------------------------------

    df["normalization"] = results.apply(
        lambda x:
        x["normalization"]
    )

    # -----------------------------------------------------
    # REPEATED CHARACTER
    # -----------------------------------------------------

    df["repeated_character"] = results.apply(
        lambda x:
        x["repeated_character"]
    )

    # -----------------------------------------------------
    # TOKEN
    # -----------------------------------------------------

    df["token"] = results.apply(
        lambda x:
        x["token"]
    )

    # -----------------------------------------------------
    # FINAL TEXT
    # -----------------------------------------------------

    df["final_text"] = results.apply(
        lambda x:
        x["final_text"]
    )

    return df


# =========================================================
# PREPROCESSING STATISTICS
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

        "Repeated Character":
            df["repeated_character"].notna().sum(),

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

    counter = Counter(
        words
    )

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

    return preprocess_text(
        text
    )


# =========================================================
# EXPORT
# =========================================================

__all__ = [

    "validate_text",

    "cleaning",

    "case_folding",

    "normalization",

    "repeated_character_handling",

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
