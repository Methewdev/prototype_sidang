"""
=========================================================
CUSTOMER SEGMENTATION MODULE
=========================================================
Emotion Probability
        ↓
Standard Scaler
        ↓
KMeans
        ↓
Customer Segment
=========================================================
"""

import pandas as pd
import numpy as np

from modules.model_loader import (
    load_scaler,
    load_kmeans
)

from config import (
    EMOTION_LABELS,
    SEGMENT_MAPPING
)

# ==========================================================
# LOAD MODEL
# ==========================================================

scaler = load_scaler()

kmeans = load_kmeans()

# ==========================================================
# SINGLE SEGMENTATION
# ==========================================================

def predict_segment(probability):

    """
    probability:
    [Frustrasi, Netral, Sedih, Senang]
    """

    probability = np.array(probability).reshape(1, -1)

    probability_scaled = scaler.transform(
        probability
    )

    cluster = int(

        kmeans.predict(
            probability_scaled
        )[0]

    )

    segment = SEGMENT_MAPPING.get(
        cluster,
        "Unknown"
    )

    return {

        "cluster": cluster,

        "segment": segment

    }

# ==========================================================
# DATAFRAME SEGMENTATION
# ==========================================================

def segment_dataframe(df):

    data = df.copy()

    X = data[
        EMOTION_LABELS
    ]

    X_scaled = scaler.transform(X)

    cluster = kmeans.predict(X_scaled)

    data["Cluster"] = cluster

    data["Customer Segment"] = [

        SEGMENT_MAPPING.get(i, "Unknown")

        for i in cluster

    ]

    return data

# ==========================================================
# SEGMENT SUMMARY
# ==========================================================

def segment_summary(df):

    summary = (

        df

        .groupby("Customer Segment")

        .size()

        .reset_index(name="Total")

    )

    return summary

# ==========================================================
# SEGMENT PROFILE
# ==========================================================

def segment_profile(df):

    profile = (

        df

        .groupby("Customer Segment")[

            EMOTION_LABELS

        ]

        .mean()

        .round(3)

    )

    return profile

# ==========================================================
# DOMINANT SEGMENT
# ==========================================================

def dominant_segment(df):

    return (

        df["Customer Segment"]

        .mode()[0]

    )

# ==========================================================
# SEGMENT DISTRIBUTION
# ==========================================================

def segment_distribution(df):

    return (

        df["Customer Segment"]

        .value_counts()

        .reset_index()

        .rename(

            columns={

                "index": "Segment",

                "Customer Segment": "Total"

            }

        )

    )

# ==========================================================
# SEGMENT PERCENTAGE
# ==========================================================

def segment_percentage(df):

    distribution = segment_distribution(df)

    distribution["Percentage"] = (

        distribution["Total"]

        / distribution["Total"].sum()

        * 100

    ).round(2)

    return distribution

# ==========================================================
# SINGLE SUMMARY
# ==========================================================

def segmentation_result(probability):

    result = predict_segment(probability)

    return {

        "Cluster": result["cluster"],

        "Customer Segment": result["segment"]

    }

# ==========================================================
# EXPORT RESULT
# ==========================================================

def export_segmentation(df):

    result = segment_dataframe(df)

    return result
