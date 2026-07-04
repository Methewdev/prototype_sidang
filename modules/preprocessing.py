"""
=========================================================
PREPROCESSING MODULE
=========================================================
Livin Emotion Analysis
=========================================================
"""

import re
import string
import pandas as pd
import nltk

from cleantext import clean

from nltk.tokenize import word_tokenize

from Sastrawi.Stemmer.StemmerFactory import (
    StemmerFactory
)

from Sastrawi.StopWordRemover.StopWordRemoverFactory import (
    StopWordRemoverFactory
)

from config import SLANG_FILE

# =====================================================
# DOWNLOAD NLTK
# =====================================================

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# =====================================================
# INITIALIZE
# =====================================================

stemmer = StemmerFactory().create_stemmer()

factory = StopWordRemoverFactory()

STOPWORDS = set(factory.get_stop_words())
# =====================================================
# LOAD SLANG DICTIONARY
# =====================================================

def load_slang_dictionary():

    if not SLANG_FILE.exists():

        raise FileNotFoundError(

            f"Kamus tidak ditemukan:\n{SLANG_FILE}"

        )

    slang_df = pd.read_csv(

        SLANG_FILE,

        header=None,

        names=[

            "slang",

            "formal"

        ],

        encoding="utf-8"

    )

    slang_df = slang_df.dropna()

    slang_df["slang"] = (

        slang_df["slang"]

        .astype(str)

        .str.lower()

        .str.strip()

    )

    slang_df["formal"] = (

        slang_df["formal"]

        .astype(str)

        .str.lower()

        .str.strip()

    )

    return dict(

        zip(

            slang_df["slang"],

            slang_df["formal"]

        )

    )


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

    # EMAIL
    text = re.sub(r"\S+@\S+", " ", text)

    # MENTION
    text = re.sub(r"@\w+", " ", text)

    # HASHTAG
    text = re.sub(r"#\w+", " ", text)

    # HTML
    text = re.sub(r"<.*?>", " ", text)

    # ANGKA
    text = re.sub(r"\d+", " ", text)

    # PUNCTUATION
    text = text.translate(

        str.maketrans(

            "",

            "",

            string.punctuation

        )

    )

    # MULTIPLE SPACE
    text = re.sub(

        r"\s+",

        " ",

        text

    )

    return text.strip()
  # =====================================================
# CASE FOLDING
# =====================================================

def case_folding(text):

    if pd.isna(text):

        return ""

    return str(text).lower()
  # =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    if pd.isna(text):

        return ""

    text = clean(

        text,

        fix_unicode=True,

        to_ascii=False,

        lower=False,

        no_urls=True,

        no_emails=True,

        no_phone_numbers=True,

        no_numbers=False,

        no_digits=False,

        no_currency_symbols=True,

        no_punct=False

    )

    text = re.sub(

        r"\s+",

        " ",

        text

    )

    return text.strip()
  # =====================================================
# LEXICAL NORMALIZATION
# =====================================================

def normalization(text):

    """
    Normalisasi kata menggunakan kamus alay
    """

    if pd.isna(text):

        return ""

    words = str(text).split()

    normalized = [

        SLANG_DICT.get(

            word,

            word

        )

        for word in words

    ]

    return " ".join(normalized)
  # =====================================================
# STOPWORD REMOVAL
# =====================================================

def stopword_removal(text):

    """
    Menghapus stopword Bahasa Indonesia
    """

    if pd.isna(text):

        return ""

    words = word_tokenize(str(text))

    words = [

        word

        for word in words

        if word not in STOPWORDS

    ]

    return " ".join(words)
  # =====================================================
# STEMMING
# =====================================================

def stemming(text):

    """
    Stemming menggunakan Sastrawi
    """

    if pd.isna(text):

        return ""

    return stemmer.stem(str(text))
  # =====================================================
# TOKENIZATION
# =====================================================

def tokenization(text):

    """
    Tokenisasi menggunakan NLTK
    """

    if pd.isna(text):

        return []

    return word_tokenize(str(text))
  # =====================================================
# FINAL TEXT
# =====================================================

def final_text(tokens):

    """
    Menggabungkan token menjadi kalimat
    """

    if len(tokens) == 0:

        return ""

    return " ".join(tokens)
