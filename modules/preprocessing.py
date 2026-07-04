"""
=========================================================
PREPROCESSING MODULE
Livin Emotion Analysis
=========================================================
"""

import re
import string
import pandas as pd

from config import SLANG_FILE
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# =====================================================
# INITIALIZE
# =====================================================

stemmer = StemmerFactory().create_stemmer()

stopword = StopWordRemoverFactory().create_stop_word_remover()

# =====================================================
# SLANG DICTIONARY
# =====================================================

def load_slang_dictionary():

    slang_df = pd.read_csv(

        SLANG_FILE,

        encoding="utf-8"

    )

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

    if text is None:
        return ""

    text = str(text)

    text = re.sub(r"http\S+", " ", text)

    text = re.sub(r"www\S+", " ", text)

    text = re.sub(r"@\w+", " ", text)

    text = re.sub(r"#\w+", " ", text)

    text = re.sub(r"\d+", " ", text)

    text = re.sub(r"[^\w\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

# =====================================================
# CASE FOLDING
# =====================================================

def case_folding(text):

    return text.lower()

# =====================================================
# NORMALIZATION
# =====================================================

def normalization(text):

    words = text.split()

    normalized = [

        SLANG_DICT.get(

            word,

            word

        )

        for word in words

    ]

    return " ".join(normalized)

# =====================================================
# TOKENIZER
# =====================================================

def tokenization(text):

    return text.split()

# =====================================================
# STOPWORD
# =====================================================

def stopword_removal(text):

    return stopword.remove(text)

# =====================================================
# STEMMING
# =====================================================

def stemming(text):

    return stemmer.stem(text)

# =====================================================
# FULL PREPROCESS
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
