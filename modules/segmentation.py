"""
=========================================================
CUSTOMER SEGMENTATION MODULE
=========================================================
"""

import streamlit as st
import pandas as pd

from config import EMOTION_LABELS


# =====================================================
# RESET PIPELINE
# =====================================================

def reset_pipeline():

    keys = [
        "preprocess_df",
        "prediction_df",
        "segmentation_df",
        "retention_df"
    ]

    for key in keys:
        if key in st.session_state:
            del st.session_state[key]


# =====================================================
# SEGMENT MAPPING
# =====================================================

SEGMENT_MAPPING = {

    "Senang": {
        "Customer Segment": "😊 Nasabah Puas",
        "Risk Level": "Low"
    },

    "Netral": {
        "Customer Segment": "😐 Nasabah Passive ",
        "Risk Level": "Medium"
    },

    "Sedih": {
        "Customer Segment": "😟 Nasabah Tidak Puas",
        "Risk Level": "High"
    },

    "Frustrasi": {
        "Customer Segment": "😠 Nasabah Frustasi",
        "Risk Level": "Very High"
    }

}

# =====================================================
# CUSTOMER SEGMENTATION
# =====================================================

def customer_segmentation(df):

    data = df.copy()

    data["Customer Segment"] = data["emotion"].map(
        lambda x: SEGMENT_MAPPING.get(
            x,
            {
                "Customer Segment": "Unknown",
                "Risk Level": "Unknown"
            }
        )["Customer Segment"]
    )

    data["Risk Level"] = data["emotion"].map(
        lambda x: SEGMENT_MAPPING.get(
            x,
            {
                "Customer Segment": "Unknown",
                "Risk Level": "Unknown"
            }
        )["Risk Level"]
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
        summary["Total"] /
        summary["Total"].sum() * 100
    ).round(2)

    return summary


# =====================================================
# DOMINANT EMOTION
# =====================================================

def dominant_emotion(df):

    return (
        df.groupby("Customer Segment")["emotion"]
        .agg(lambda x: x.mode().iloc[0])
    )


# =====================================================
# SEGMENT STATISTICS
# =====================================================

def segment_statistics(df):

    return {

        "Total Customer": len(df),

        "Total Segment":
            df["Customer Segment"].nunique(),

        "Dominant Segment":
            df["Customer Segment"].mode().iloc[0]

    }


# =====================================================
# CLUSTER PROFILE
# =====================================================

def cluster_profile(df):

    cols = [
        c for c in EMOTION_LABELS
        if c in df.columns
    ]

    if len(cols) == 0:
        return pd.DataFrame()

    return (
        df.groupby("Customer Segment")[cols]
        .mean()
        .round(3)
    )


# =====================================================
# SEGMENT DISTRIBUTION
# =====================================================

def segment_distribution(df):

    return (
        df["Customer Segment"]
        .value_counts()
    )


# =====================================================
# SILHOUETTE
# =====================================================

def silhouette(df):
    """
    Placeholder.
    Karena segmentasi menggunakan rule-based,
    Silhouette Score tidak dihitung.
    """

    return 1.0


__all__ = [

    "customer_segmentation",

    "segment_summary",

    "dominant_emotion",

    "segment_statistics",

    "cluster_profile",

    "segment_distribution",

    "silhouette",

    "reset_pipeline"

]
