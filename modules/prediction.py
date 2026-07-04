"""
=========================================================
PREDICTION MODULE
Fine-Tuned IndoBERT
=========================================================
"""

import numpy as np
import pandas as pd
import torch

from modules.loader import load_model
from config import MAX_LENGTH, EMOTION_LABELS

# =====================================================
# LOAD MODEL
# =====================================================

tokenizer, model, device = load_model()

# =====================================================
# SINGLE PREDICTION
# =====================================================

def predict_text(text):

    encoding = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH
    )

    encoding = {
        k: v.to(device)
        for k, v in encoding.items()
    }

    with torch.no_grad():

        output = model(**encoding)

    probability = torch.softmax(
        output.logits,
        dim=1
    ).cpu().numpy()[0]

    prediction = int(np.argmax(probability))

    emotion = EMOTION_LABELS[prediction]

    confidence = float(probability[prediction])

    return emotion, confidence, probability
