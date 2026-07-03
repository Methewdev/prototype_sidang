"""
=========================================================
MODEL LOADER
=========================================================
Production Ready
=========================================================
"""

import joblib
import streamlit as st
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from config import (
    HF_MODEL,
    SCALER,
    KMEANS,
    LABEL_ENCODER
)

# ==========================================================
# DEVICE
# ==========================================================

@st.cache_resource
def get_device():

    if torch.cuda.is_available():

        return torch.device("cuda")

    return torch.device("cpu")


# ==========================================================
# TOKENIZER
# ==========================================================

@st.cache_resource
def load_tokenizer():

    tokenizer = AutoTokenizer.from_pretrained(
        HF_MODEL
    )

    return tokenizer


# ==========================================================
# MODEL
# ==========================================================

@st.cache_resource
def load_model():

    device = get_device()

    model = AutoModelForSequenceClassification.from_pretrained(
        HF_MODEL
    )

    model.to(device)

    model.eval()

    return model


# ==========================================================
# LABEL ENCODER
# ==========================================================

@st.cache_resource
def load_label_encoder():

    return joblib.load(
        LABEL_ENCODER
    )


# ==========================================================
# SCALER
# ==========================================================

@st.cache_resource
def load_scaler():

    return joblib.load(
        SCALER
    )


# ==========================================================
# KMEANS
# ==========================================================

@st.cache_resource
def load_kmeans():

    return joblib.load(
        KMEANS
    )


# ==========================================================
# LOAD ALL
# ==========================================================

@st.cache_resource
def load_all():

    tokenizer = load_tokenizer()

    model = load_model()

    label_encoder = load_label_encoder()

    scaler = load_scaler()

    kmeans = load_kmeans()

    return (

        tokenizer,

        model,

        label_encoder,

        scaler,

        kmeans

    )


# ==========================================================
# MODEL INFORMATION
# ==========================================================

def model_information():

    device = get_device()

    return {

        "Model":HF_MODEL,

        "Device":str(device),

        "Framework":"PyTorch",

        "Transformer":"IndoBERT"

    }


# ==========================================================
# CLEAR CACHE
# ==========================================================

def clear_cache():

    st.cache_resource.clear()
