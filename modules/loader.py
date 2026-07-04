"""
=========================================================
MODEL LOADER
=========================================================
Fine-Tuned IndoBERT
=========================================================
"""

import streamlit as st
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from config import (
    MODEL_NAME,
    MODEL_PATH,
    USE_LOCAL_MODEL
)

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource(show_spinner="Loading Emotion Model...")
def load_model():

    # ==========================================
    # DEVICE
    # ==========================================

    device = torch.device(

        "cuda"

        if torch.cuda.is_available()

        else "cpu"

    )

    # ==========================================
    # LOCAL MODEL
    # ==========================================

    if USE_LOCAL_MODEL:

        tokenizer = AutoTokenizer.from_pretrained(

            MODEL_PATH,

            local_files_only=True

        )

        model = AutoModelForSequenceClassification.from_pretrained(

            MODEL_PATH,

            local_files_only=True

        )

    # ==========================================
    # HUGGINGFACE
    # ==========================================

    else:

        tokenizer = AutoTokenizer.from_pretrained(

            MODEL_NAME

        )

        model = AutoModelForSequenceClassification.from_pretrained(

            MODEL_NAME

        )

    model.to(device)

    model.eval()

    return tokenizer, model, device
