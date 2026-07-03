"""
=========================================================
CONFIGURATION
Livin Emotion Analysis Dashboard
=========================================================
"""

import os

# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "Livin Emotion Analysis"

APP_VERSION = "1.0.0"

AUTHOR = "Herdi"

# ==========================================================
# PAGE
# ==========================================================

PAGE_TITLE = "Livin Emotion Analysis Dashboard"

PAGE_ICON = "📊"

LAYOUT = "wide"

INITIAL_SIDEBAR_STATE = "expanded"

FOOTER = "© 2026 Livin Emotion Analysis"

# ==========================================================
# PATH
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "models")

DATA_DIR = os.path.join(BASE_DIR, "data")

ASSET_DIR = os.path.join(BASE_DIR, "assets")

CSS = os.path.join(ASSET_DIR, "style.css")

LOGO = os.path.join(ASSET_DIR, "logo.png")

# ==========================================================
# HUGGING FACE
# ==========================================================

HF_MODEL = "username/livin-emotion-indobert"

# contoh:
# HF_MODEL = "envidevelopment/livin-emotion-indobert"

# ==========================================================
# TOKENIZER
# ==========================================================

MAX_LENGTH = 128

TRUNCATION = True

PADDING = "max_length"

RETURN_TENSOR = "pt"

# ==========================================================
# EMOTION LABEL
# ==========================================================

EMOTION_LABELS = [

    "Frustrasi",

    "Netral",

    "Sedih",

    "Senang"

]

NUM_LABEL = len(EMOTION_LABELS)

# ==========================================================
# EMOTION COLOR
# ==========================================================

EMOTION_COLOR = {

    "Frustrasi": "#EF4444",

    "Netral": "#FACC15",

    "Sedih": "#3B82F6",

    "Senang": "#22C55E"

}

# ==========================================================
# SEGMENT
# ==========================================================

SEGMENT_MAPPING = {

    0: "Satisfied Customer",

    1: "Passive Customer",

    2: "At-Risk Customer"

}

# ==========================================================
# RETENTION
# ==========================================================

RETENTION = {

    "Satisfied Customer":{

        "Priority":"Low",

        "Recommendation":
        "Pertahankan loyalitas pelanggan melalui reward, cashback, dan promo eksklusif."

    },

    "Passive Customer":{

        "Priority":"Medium",

        "Recommendation":
        "Dorong penggunaan fitur melalui edukasi dan personalisasi promo."

    },

    "At-Risk Customer":{

        "Priority":"High",

        "Recommendation":
        "Prioritaskan penyelesaian keluhan dan tingkatkan kualitas layanan."

    }

}

# ==========================================================
# MODEL FILE
# ==========================================================

SCALER = os.path.join(

    MODEL_DIR,

    "scaler.pkl"

)

KMEANS = os.path.join(

    MODEL_DIR,

    "kmeans.pkl"

)

LABEL_ENCODER = os.path.join(

    MODEL_DIR,

    "label_encoder.pkl"

)

# ==========================================================
# SESSION STATE
# ==========================================================

SESSION = {

    "RAW":"raw_df",

    "UNDERSTANDING":"understanding_df",

    "CLEAN":"clean_df",

    "CASE":"case_df",

    "NORMAL":"normal_df",

    "TOKEN":"token_df",

    "PREDICTION":"prediction_df",

    "PROBABILITY":"probability_df",

    "SEGMENT":"segment_df",

    "RETENTION":"retention_df"

}

# ==========================================================
# DATASET COLUMN
# ==========================================================

TEXT_COLUMNS = [

    "content",

    "review",

    "ulasan",

    "text"

]

SCORE_COLUMNS = [

    "score",

    "rating"

]

DATE_COLUMNS = [

    "at",

    "date",

    "tanggal"

]

# ==========================================================
# OUTPUT COLUMN
# ==========================================================

OUTPUT = {

    "TEXT":"normalization",

    "EMOTION":"emotion",

    "CONFIDENCE":"confidence",

    "SEGMENT":"Customer Segment",

    "PRIORITY":"Priority"

}

# ==========================================================
# CACHE
# ==========================================================

CACHE_MODEL = True

CACHE_DATA = True

# ==========================================================
# EXPORT
# ==========================================================

CSV_ENCODING = "utf-8-sig"

EXPORT_NAME = "Livin_Emotion_Result.csv"

# ==========================================================
# RANDOM
# ==========================================================

RANDOM_STATE = 42

N_CLUSTER = 3

# ==========================================================
# VERSION
# ==========================================================

MODEL_NAME = "Fine-Tuned IndoBERT"

SEGMENT_MODEL = "KMeans"

DEPLOYMENT = "Streamlit Community Cloud"
