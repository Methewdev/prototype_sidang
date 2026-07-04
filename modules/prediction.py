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
# PREDICT SINGLE TEXT
# =====================================================

def predict_text(text):

    """
    Predict emotion from a single text.
    """

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

    prediction = int(

        np.argmax(probability)

    )

    emotion = EMOTION_LABELS[prediction]

    confidence = float(

        probability[prediction]

    )

    return {

        "emotion": emotion,

        "confidence": confidence,

        "probability": probability

    }
  # =====================================================
# PREDICT BATCH
# =====================================================

def predict_batch(texts):

    if len(texts) == 0:

        return []

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

        prediction = np.argmax(

            probs,

            axis=1

        )

        for pred, prob in zip(

            prediction,

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

    return {

        "Total Review":

            len(df),

        "Dominant Emotion":

            df["emotion"]

            .mode()[0],

        "Average Confidence":

            round(

                df["confidence"]

                .mean()

                *100,

                2

            )

    }
