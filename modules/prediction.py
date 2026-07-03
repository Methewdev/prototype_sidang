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
