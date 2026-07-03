"""
=========================================================
MODEL LOADER
=========================================================
"""

import streamlit as st
import torch
import joblib

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from config import *

# =========================================================
# DEVICE
# =========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# =========================================================
# LOAD TOKENIZER
# =========================================================

@st.cache_resource
def load_tokenizer():

    tokenizer = AutoTokenizer.from_pretrained(
        HF_MODEL
    )

    return tokenizer


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    model = AutoModelForSequenceClassification.from_pretrained(
        HF_MODEL
    )

    model.to(DEVICE)

    model.eval()

    return model


# =========================================================
# LOAD LABEL ENCODER
# =========================================================

@st.cache_resource
def load_label_encoder():

    return joblib.load(
        LABEL_ENCODER_PATH
    )


# =========================================================
# LOAD SCALER
# =========================================================

@st.cache_resource
def load_scaler():

    return joblib.load(
        SCALER_PATH
    )


# =========================================================
# LOAD KMEANS
# =========================================================

@st.cache_resource
def load_kmeans():

    return joblib.load(
        KMEANS_PATH
    )


# =========================================================
# LOAD ALL
# =========================================================

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


# =========================================================
# GET DEVICE
# =========================================================

def get_device():

    return DEVICE


# =========================================================
# MODEL INFO
# =========================================================

def get_model_information():

    model = load_model()

    info = {

        "Model Name":HF_MODEL,

        "Device":str(DEVICE),

        "Number of Labels":model.config.num_labels,

        "Maximum Length":MAX_LENGTH,

        "Emotion Labels":EMOTION_LABELS

    }

    return info


# =========================================================
# CHECK MODEL
# =========================================================

def check_model():

    try:

        tokenizer = load_tokenizer()

        model = load_model()

        return True

    except Exception as e:

        st.error(e)

        return False


# =========================================================
# WARMUP
# =========================================================

def warmup():

    tokenizer = load_tokenizer()

    model = load_model()

    sample = "Aplikasi Livin sangat membantu transaksi saya"

    inputs = tokenizer(

        sample,

        return_tensors="pt",

        truncation=True,

        padding=True,

        max_length=MAX_LENGTH

    )

    inputs = {

        k:v.to(DEVICE)

        for k,v in inputs.items()

    }

    with torch.no_grad():

        _ = model(**inputs)

    return True


# =========================================================
# LOAD STATUS
# =========================================================

def model_status():

    status = {

        "Tokenizer":"Loaded",

        "Model":"Loaded",

        "Label Encoder":"Loaded",

        "Scaler":"Loaded",

        "KMeans":"Loaded"

    }

    return status
