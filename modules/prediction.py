"""
=========================================================
PREDICTION MODULE
Production Ready
=========================================================
"""

import torch
import numpy as np
import pandas as pd

from modules.model_loader import (
    load_model,
    load_tokenizer,
    get_device
)

from config import (
    MAX_LENGTH,
    OUTPUT
)

# ==========================================================
# LOAD RESOURCE
# ==========================================================

tokenizer = load_tokenizer()

model = load_model()

device = get_device()

# ==========================================================
# SINGLE PREDICTION
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

        logits = model(**encoding).logits

    probability = torch.softmax(

        logits,

        dim=1

    ).cpu().numpy()[0]

    prediction = int(

        np.argmax(probability)

    )

    label = model.config.id2label[prediction]

    return {

        "emotion":label,

        "confidence":float(np.max(probability)),

        "probability":probability

    }
# ==========================================================
# BATCH PREDICTION
# ==========================================================

def predict_batch(

    texts,

    batch_size=32,

    progress_callback=None

):

    all_emotion=[]

    all_confidence=[]

    all_probability=[]

    total=len(texts)

    for start in range(

        0,

        total,

        batch_size

    ):

        end=min(

            start+batch_size,

            total

        )

        batch=texts[start:end]

        encoding=tokenizer(

            batch,

            padding=True,

            truncation=True,

            max_length=MAX_LENGTH,

            return_tensors="pt"

        )

        encoding={

            k:v.to(device)

            for k,v in encoding.items()

        }

        with torch.no_grad():

            logits=model(**encoding).logits

        probability=torch.softmax(

            logits,

            dim=1

        ).cpu().numpy()

        prediction=np.argmax(

            probability,

            axis=1

        )

        for pred,prob in zip(

            prediction,

            probability

        ):

            label=model.config.id2label[int(pred)]

            all_emotion.append(label)

            all_confidence.append(

                float(np.max(prob))

            )

            all_probability.append(prob)

        if progress_callback:

            progress_callback(end,total)

    return (

        all_emotion,

        all_confidence,

        all_probability

    )
# ==========================================================
# DATAFRAME
# ==========================================================

def predict_dataframe(

    df,

    text_column="normalization",

    batch_size=32,

    progress_callback=None

):

    data=df.copy()

    texts=data[text_column].astype(str).tolist()

    emotion,confidence,probability=\
        predict_batch(

            texts,

            batch_size,

            progress_callback

        )

    data["emotion"]=emotion

    data["confidence"]=confidence
    probability=np.array(probability)

    labels=[

        model.config.id2label[i]

        for i in range(

            probability.shape[1]

        )

    ]

    for idx,label in enumerate(labels):

        data[label]=probability[:,idx]

    return data
    # ==========================================================
# PROBABILITY
# ==========================================================

def predict_probability(text):

    result=predict(text)

    probability=result["probability"]

    labels=[

        model.config.id2label[i]

        for i in range(

            len(probability)

        )

    ]

    return {

        label:float(prob)

        for label,prob

        in zip(

            labels,

            probability

        )

    }
    # ==========================================================
# SUMMARY
# ==========================================================

def prediction_summary(df):

    return{

        "Total Review":len(df),

        "Dominant Emotion":

        df["emotion"].mode()[0],

        "Average Confidence":

        round(

            df["confidence"].mean()*100,

            2

        )

    }
