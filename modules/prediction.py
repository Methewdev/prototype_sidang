"""
=========================================================
PREDICTION MODULE
Fine-Tuned IndoBERT Emotion Classification
=========================================================
"""

import numpy as np
import pandas as pd
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
model.eval()

# =====================================================
# VALIDATE TEXT
# =====================================================

def validate_prediction_text(text):

    if text is None:
        return ""

    return str(text).strip()


# =====================================================
# FORMAT PROBABILITY
# =====================================================

def format_probability(probability):

    return {

        label: float(prob)

        for label, prob in zip(

            EMOTION_LABELS,

            probability

        )

    }


# =====================================================
# PREDICT SINGLE TEXT
# =====================================================

def predict_text(text):

    text = validate_prediction_text(text)

    if text == "":

        return {

            "emotion": "-",

            "confidence": 0.0,

            "probability": {

                label: 0.0

                for label in EMOTION_LABELS

            }

        }

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

    prediction = int(

        np.argmax(probability)

    )

    return {

        "emotion": EMOTION_LABELS[prediction],

        "confidence": float(probability[prediction]),

        "probability": format_probability(probability)

    }


# =====================================================
# PREDICT SINGLE REVIEW
# =====================================================

def predict_single_review(text):

    return predict_text(text)


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

        key: value.to(device)

        for key, value in encoding.items()

    }

    with torch.no_grad():

        output = model(**encoding)

    probability = torch.softmax(

        output.logits,

        dim=1

    ).cpu().numpy()

    return probability


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

    texts = (

        data[text_column]

        .fillna("")

        .astype(str)

        .tolist()

    )

    emotion_result = []

    confidence_result = []

    probability_result = []

    for start in range(

        0,

        len(texts),

        batch_size

    ):

        batch = texts[

            start:start+batch_size

        ]

        probs = predict_batch(batch)

        predictions = np.argmax(

            probs,

            axis=1

        )

        for pred, prob in zip(

            predictions,

            probs

        ):

            emotion_result.append(

                EMOTION_LABELS[pred]

            )

            confidence_result.append(

                float(prob[pred])

            )

            probability_result.append(prob)

    probability_result = np.array(

        probability_result

    )

    data["emotion"] = emotion_result

    data["confidence"] = confidence_result

    for i, label in enumerate(

        EMOTION_LABELS

    ):

        data[label] = probability_result[:, i]

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
# TOP PREDICTION
# =====================================================

def top_prediction(result):

    return {

        "emotion": result["emotion"],

        "confidence": round(

            result["confidence"] * 100,

            2

        )

    }


# =====================================================
# EXPORT
# =====================================================

__all__ = [

    "predict_text",

    "predict_single_review",

    "predict_batch",

    "predict_dataframe",

    "prediction_summary",

    "top_prediction"

]
