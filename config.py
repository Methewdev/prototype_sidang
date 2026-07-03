"""
==========================================================
CONFIGURATION
Livin Emotion Analysis Dashboard
==========================================================
"""

import os

# ==========================================================
# PROJECT
# ==========================================================

PROJECT_NAME = "Livin Emotion Analysis Dashboard"

VERSION = "1.0.0"

AUTHOR = "Herdi"

DESCRIPTION = """
Emotion Classification menggunakan Fine-Tuned IndoBERT,
Customer Segmentation menggunakan KMeans,
dan Customer Retention Recommendation.
"""

# ==========================================================
# HUGGING FACE MODEL
# ==========================================================

# Ganti sesuai repository Anda
HF_MODEL = "username/livin-emotion-indobert"

# Contoh:
# HF_MODEL = "envidevelopment/livin-emotion-indobert"

MAX_LENGTH = 128

DEVICE = "cpu"

# ==========================================================
# LABEL EMOTION
# ==========================================================

EMOTION_LABELS = [

    "Frustrasi",

    "Netral",

    "Sedih",

    "Senang"

]

NUM_LABELS = len(EMOTION_LABELS)

LABEL2ID = {

    "Frustrasi":0,

    "Netral":1,

    "Sedih":2,

    "Senang":3

}

ID2LABEL = {

    0:"Frustrasi",

    1:"Netral",

    2:"Sedih",

    3:"Senang"

}

# ==========================================================
# MODEL DIRECTORY
# ==========================================================

MODEL_DIR = "models"

LABEL_ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "label_encoder.pkl"
)

SCALER_PATH = os.path.join(
    MODEL_DIR,
    "scaler.pkl"
)

KMEANS_PATH = os.path.join(
    MODEL_DIR,
    "kmeans.pkl"
)

# ==========================================================
# DATA
# ==========================================================

DATA_DIR = "data"

SAMPLE_DATA = os.path.join(
    DATA_DIR,
    "sample_review.csv"
)

# ==========================================================
# STREAMLIT
# ==========================================================

PAGE_TITLE = "Livin Emotion Analysis"

PAGE_ICON = "📊"

LAYOUT = "wide"

INITIAL_SIDEBAR_STATE = "expanded"

# ==========================================================
# DASHBOARD COLOR
# ==========================================================

PRIMARY_COLOR = "#1E88E5"

SUCCESS_COLOR = "#43A047"

WARNING_COLOR = "#FB8C00"

DANGER_COLOR = "#E53935"

BACKGROUND_COLOR = "#F5F5F5"

TEXT_COLOR = "#212121"

# ==========================================================
# CHART COLOR
# ==========================================================

EMOTION_COLOR = {

    "Senang":"#4CAF50",

    "Netral":"#2196F3",

    "Sedih":"#FB8C00",

    "Frustrasi":"#F44336"

}

# ==========================================================
# CUSTOMER SEGMENT
# ==========================================================

SEGMENT_MAPPING = {

    0:"Satisfied Customer",

    1:"Passive Customer",

    2:"At-Risk Customer"

}

# ==========================================================
# RETENTION STRATEGY
# ==========================================================

RETENTION = {

    "Satisfied Customer":{

        "Priority":"Low",

        "Recommendation":
        """
        Pertahankan loyalitas pelanggan melalui
        reward, cashback, dan promo eksklusif.
        """

    },

    "Passive Customer":{

        "Priority":"Medium",

        "Recommendation":
        """
        Tingkatkan engagement melalui edukasi fitur,
        campaign, dan personalisasi layanan.
        """

    },

    "At-Risk Customer":{

        "Priority":"High",

        "Recommendation":
        """
        Prioritaskan penyelesaian keluhan,
        peningkatan stabilitas aplikasi,
        dan customer support proaktif.
        """

    }

}

# ==========================================================
# KMEANS
# ==========================================================

N_CLUSTER = 3

RANDOM_STATE = 42

# ==========================================================
# PREPROCESSING
# ==========================================================

REMOVE_URL = True

REMOVE_HTML = True

REMOVE_NUMBER = True

REMOVE_PUNCTUATION = True

REMOVE_EMOJI = True

REMOVE_EXTRA_SPACE = True

LOWERCASE = True

STEMMING = True

STOPWORD = True

NORMALIZATION = True

# ==========================================================
# FILE
# ==========================================================

SUPPORTED_FILE = [

    "csv",

    "xlsx"

]

# ==========================================================
# COLUMN
# ==========================================================

TEXT_COLUMN = "review"

OUTPUT_COLUMN = "emotion"

CONFIDENCE_COLUMN = "confidence"

SEGMENT_COLUMN = "Customer Segment"

# ==========================================================
# VISUALIZATION
# ==========================================================

PIE_HEIGHT = 450

BAR_HEIGHT = 450

WORDCLOUD_WIDTH = 900

WORDCLOUD_HEIGHT = 500

# ==========================================================
# BATCH PREDICTION
# ==========================================================

BATCH_SIZE = 32

# ==========================================================
# DOWNLOAD
# ==========================================================

OUTPUT_FILE = "Emotion_Analysis_Result.csv"

# ==========================================================
# SIDEBAR
# ==========================================================

MENU = [

    "Dashboard",

    "Single Prediction",

    "Batch Prediction",

    "Customer Segmentation"

]

# ==========================================================
# FOOTER
# ==========================================================

FOOTER = """
Developed using

✅ IndoBERT

✅ HuggingFace

✅ Streamlit

✅ Scikit-Learn
"""

# ==========================================================
# LOGO
# ==========================================================

LOGO = "assets/logo.png"

CSS = "assets/style.css"

print("="*60)
print(PROJECT_NAME)
print(VERSION)
print("Configuration Loaded")
print("="*60)
