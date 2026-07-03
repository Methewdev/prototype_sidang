"""
=========================================================
EMOTION PREDICTION MODULE
=========================================================
Fine-Tuned IndoBERT
=========================================================
"""

import torch
import pandas as pd
import numpy as np

from modules.model_loader import (
    load_all,
    get_device
)

from config import MAX_LENGTH

# ==========================================================
# LOAD MODEL
# ==========================================================

tokenizer, model, label_encoder, scaler, kmeans = load_all()

device = get_device()

# ==========================================================
# PREDICT SINGLE TEXT
# ==========================================================

def predict(text):

    encoding = tokenizer(

        text,

        return_tensors="pt",

        truncation=True,

        padding="max_length",

        max_length=MAX_LENGTH

    )

    encoding = {

        k:v.to(device)

        for k,v in encoding.items()

    }

    with torch.no_grad():

        outputs = model(**encoding)

    logits = outputs.logits

    probability = torch.softmax(

        logits,

        dim=1

    )

    probability = probability.cpu().numpy()[0]

    prediction = np.argmax(probability)

    emotion = label_encoder.inverse_transform(

        [prediction]

    )[0]

    confidence = float(

        np.max(probability)

    )

    return {

        "emotion":emotion,

        "confidence":confidence,

        "probability":probability

    }

# ==========================================================
# PREDICT PROBABILITY
# ==========================================================

def predict_probability(text):

    result = predict(text)

    probability = result["probability"]

    return {

        "Frustrasi":float(probability[0]),

        "Netral":float(probability[1]),

        "Sedih":float(probability[2]),

        "Senang":float(probability[3])

    }

# ==========================================================
# PREDICT DATAFRAME
# ==========================================================

def predict_dataframe(df,column="processed_text"):

    df = df.copy()

    emotion = []

    confidence = []

    frustration=[]

    neutral=[]

    sadness=[]

    happiness=[]

    for text in df[column]:

        result = predict(str(text))

        prob = result["probability"]

        emotion.append(

            result["emotion"]

        )

        confidence.append(

            result["confidence"]

        )

        frustration.append(

            float(prob[0])

        )

        neutral.append(

            float(prob[1])

        )

        sadness.append(

            float(prob[2])

        )

        happiness.append(

            float(prob[3])

        )

    df["emotion"] = emotion

    df["confidence"] = confidence

    df["Frustrasi"] = frustration

    df["Netral"] = neutral

    df["Sedih"] = sadness

    df["Senang"] = happiness

    return df

# ==========================================================
# TOP EMOTION
# ==========================================================

def top_emotion(text):

    result = predict(text)

    return result["emotion"]

# ==========================================================
# CONFIDENCE
# ==========================================================

def confidence_score(text):

    result = predict(text)

    return round(

        result["confidence"]*100,

        2

    )

# ==========================================================
# EMOTION TABLE
# ==========================================================

def emotion_table(text):

    result = predict_probability(text)

    df = pd.DataFrame({

        "Emotion":[

            "Frustrasi",

            "Netral",

            "Sedih",

            "Senang"

        ],

        "Probability":[

            result["Frustrasi"],

            result["Netral"],

            result["Sedih"],

            result["Senang"]

        ]

    })

    return df

# ==========================================================
# PREDICTION SUMMARY
# ==========================================================

def prediction_summary(text):

    result = predict(text)

    summary = {

        "Emotion":result["emotion"],

        "Confidence":round(

            result["confidence"]*100,

            2

        ),

        "Probability":result["probability"]

    }

    return summary

# ==========================================================
# BATCH SUMMARY
# ==========================================================

def batch_summary(df):

    total = len(df)

    dominant = df["emotion"].mode()[0]

    average = round(

        df["confidence"].mean()*100,

        2

    )

    return {

        "Total Review":total,

        "Dominant Emotion":dominant,

        "Average Confidence":average

    }

# ==========================================================
# PREDICT SAMPLE
# ==========================================================

def sample_prediction():

    text = "Aplikasi Livin sangat membantu transaksi saya"

    return prediction_summary(text)
