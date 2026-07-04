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
    # =====================================================
# BATCH PREDICTION
# =====================================================

def predict_dataframe(
    df,
    text_column="final_text",
    batch_size=32
):

    data = df.copy()

    texts = data[text_column].fillna("").tolist()

    emotion_result = []
    confidence_result = []
    probability_result = []

    for start in range(0, len(texts), batch_size):

        batch = texts[start:start + batch_size]

        encoding = tokenizer(

            batch,

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

            output = model(**encoding)

        probability = torch.softmax(

            output.logits,

            dim=1

        ).cpu().numpy()

        prediction = np.argmax(

            probability,

            axis=1

        )

        for pred, prob in zip(prediction, probability):

            emotion_result.append(
                EMOTION_LABELS[pred]
            )

            confidence_result.append(
                float(prob[pred])
            )

            probability_result.append(prob)

    probability_result = np.array(probability_result)

    data["emotion"] = emotion_result

    data["confidence"] = confidence_result

    for i, label in enumerate(EMOTION_LABELS):

        data[label] = probability_result[:, i]

    return data
    # =====================================================
# SUMMARY
# =====================================================

def prediction_summary(df):

    summary = {

        "Total Review": len(df),

        "Dominant Emotion": df["emotion"].mode()[0],

        "Average Confidence": round(

            df["confidence"].mean() * 100,

            2

        )

    }

    return summary
