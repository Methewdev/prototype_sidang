"""
=========================================================
CUSTOMER SEGMENTATION
=========================================================
"""

import joblib
import pandas as pd

from config import (
    MODEL_PATH,
    EMOTION_LABELS
)

# =====================================================
# LOAD MODEL
# =====================================================

scaler = joblib.load(
    MODEL_PATH / "scaler.pkl"
)

kmeans = joblib.load(
    MODEL_PATH / "kmeans.pkl"
)

# =====================================================
# SEGMENT NAME
# =====================================================

SEGMENT_NAME = {

    0: "Satisfied Customer",

    1: "Passive Customer",

    2: "At-Risk Customer"

}
