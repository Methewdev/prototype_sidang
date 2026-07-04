"""
=========================================================
PREDICTION MODULE
Fine-Tuned IndoBERT Emotion Classification
=========================================================
"""

import numpy as np
import torch

from modules.loader import load_model
from config import (
    MAX_LENGTH,
    EMOTION_LABELS
)

# =====================================================
# LOAD MODEL
# =====================================================

tokenizer, model, device = load_model()

# =====================================================
# PREDICT SINGLE TEXT
# =====================================================

def predict_text(text):

    if text is None:
        text = ""

    text = str(text).strip()

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
        outputs = model(**encoding)

    probabilities = torch.softmax(
        outputs.logits,
        dim=1
    ).cpu().numpy()[0]

    prediction = np.argmax(probabilities)

    return {
        "emotion": EMOTION_LABELS[prediction],
        "confidence": float(probabilities[prediction]),
        "probability": probabilities
    }


# =====================================================
# PREDICT BATCH
# =====================================================

def predict_batch(texts):

    if len(texts) == 0:
        return np.array([])

    encoding = tokenizer(
        texts,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    )

    encoding = {
        k: v.to(device)
        for k, v in encoding.items()
    }

    with torch.no_grad():
        outputs = model(**encoding)

    probabilities = torch.softmax(
        outputs.logits,
        dim=1
    ).cpu().numpy()

    return probabilities


# =====================================================
# PREDICT DATAFRAME
# =====================================================

def predict_dataframe(
    df,
    text_column="final_text",
    batch_size=32
):

    data = df.copy()

    if text_column not in data.columns:
        raise ValueError(
            f"Kolom '{text_column}' tidak ditemukan."
        )

    if data.empty:
        return data

    texts = (
        data[text_column]
        .fillna("")
        .astype(str)
        .tolist()
    )

    emotions = []
    confidences = []
    probabilities = []

    for start in range(0, len(texts), batch_size):

        batch = texts[start:start + batch_size]

        probs = predict_batch(batch)

        if len(probs) == 0:
            continue

        preds = np.argmax(
            probs,
            axis=1
        )

        for pred, prob in zip(preds, probs):

            emotions.append(
                EMOTION_LABELS[pred]
            )

            confidences.append(
                round(float(prob[pred]), 4)
            )

            probabilities.append(prob)

    probabilities = np.array(probabilities)

    data.insert(
        0,
        "prediction_id",
        range(1, len(data) + 1)
    )

    data["emotion"] = emotions
    data["confidence"] = confidences

    for i, label in enumerate(EMOTION_LABELS):
        data[label] = probabilities[:, i]

    return data


# =====================================================
# SUMMARY
# =====================================================

def prediction_summary(df):

    if df.empty:

        return {
            "Total Review": 0,
            "Dominant Emotion": "-",
            "Average Confidence": 0
        }

    return {

        "Total Review": len(df),

        "Dominant Emotion": df["emotion"].mode()[0],

        "Average Confidence": round(
            df["confidence"].mean() * 100,
            2
        )

    }


# =====================================================
# EXPORT
# =====================================================

__all__ = [
    "predict_text",
    "predict_batch",
    "predict_dataframe",
    "prediction_summary"
]

# =====================================================
# PREDICT SINGLE TEXT
# =====================================================

def predict_text(text):

    if text is None:
        text = ""

    text = str(text).strip()

    encoding = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH
    )

    encoding = {
        key: value.to(device)
        for key, value in encoding.items()
    }

    with torch.no_grad():
        output = model(**encoding)

    probability = torch.softmax(
        output.logits,
        dim=1
    ).cpu().numpy()[0]

    prediction = int(np.argmax(probability))

    return {
        "emotion": EMOTION_LABELS[prediction],
        "confidence": float(probability[prediction]),
        "probability": {
            label: float(prob)
            for label, prob in zip(
                EMOTION_LABELS,
                probability
            )
        }
    }
