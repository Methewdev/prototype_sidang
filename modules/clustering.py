"""
=========================================================
CUSTOMER SEGMENTATION
=========================================================
"""

import joblib
import pandas as pd

from config import (
    MODEL_PATH,
    EMOTION_LABELS
)

# =====================================================
# LOAD MODEL
# =====================================================

scaler = joblib.load(
    MODEL_PATH / "scaler.pkl"
)

kmeans = joblib.load(
    MODEL_PATH / "kmeans.pkl"
)

# =====================================================
# SEGMENT NAME
# =====================================================

SEGMENT_NAME = {

    0: "Satisfied Customer",

    1: "Passive Customer",

    2: "At-Risk Customer"

}
# =====================================================
# SEGMENTATION
# =====================================================

def customer_segmentation(df):

    data = df.copy()

    X = data[EMOTION_LABELS]

    X_scaled = scaler.transform(X)

    cluster = kmeans.predict(X_scaled)

    data["cluster"] = cluster

    data["Customer Segment"] = (

        data["cluster"]

        .map(

            SEGMENT_NAME

        )

    )

    return data
    # =====================================================
# SEGMENT SUMMARY
# =====================================================

def segment_summary(df):

    summary = (

        df["Customer Segment"]

        .value_counts()

        .reset_index()

    )

    summary.columns = [

        "Customer Segment",

        "Total"

    ]

    summary["Percentage"] = (

        summary["Total"]

        /

        summary["Total"].sum()

        *100

    ).round(2)

    return summary
    # =====================================================
# PROFILE
# =====================================================

def cluster_profile(df):

    profile = (

        df

        .groupby(

            "Customer Segment"

        )[EMOTION_LABELS]

        .mean()

        .round(3)

    )

    return profile
    # =====================================================
# DOMINANT EMOTION
# =====================================================

def dominant_emotion(df):

    profile = cluster_profile(df)

    result = {}

    for segment in profile.index:

        emotion = (

            profile

            .loc[segment]

            .idxmax()

        )

        result[segment] = emotion

    return result
    # =====================================================
# SEGMENT STATISTICS
# =====================================================

def segment_statistics(df):

    return {

        "Total Customer":len(df),

        "Total Segment":

        df["Customer Segment"].nunique(),

        "Dominant Segment":

        df["Customer Segment"].mode()[0]

    }
