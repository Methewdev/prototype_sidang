"""
=========================================================
PREPROCESSING MODULE
Livin Emotion Analysis
=========================================================
"""

import re
import string
import unicodedata

import pandas as pd
import nltk

from cleantext import clean

from nltk.tokenize import word_tokenize

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
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

stop_factory = StopWordRemoverFactory()

stopwords = set(
    stop_factory.get_stop_words()
)
load_slang_dictionary()
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

    # HTML
    text = re.sub(r"<.*?>", " ", text)

    # Emoji
    text = re.sub(r"[^\w\s]", " ", text)

    # Angka
    text = re.sub(r"\d+", " ", text)

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

        no_line_breaks=True,

        no_urls=True,

        no_emails=True,

        no_phone_numbers=True,

        no_numbers=False,

        no_digits=False,

        no_currency_symbols=True,

        no_punct=False

    )

    text = unicodedata.normalize(

        "NFKC",

        text

    )

    text = re.sub(

        r"\s+",

        " ",

        text

    )

    return text.strip()
