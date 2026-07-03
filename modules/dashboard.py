"""
=========================================================
DASHBOARD MODULE
=========================================================
Dashboard Analytics
=========================================================
"""

import pandas as pd

from modules.visualization import (
    emotion_pie,
    emotion_bar,
    segment_bar,
    segment_pie,
    priority_bar,
    confidence_histogram,
    probability_heatmap,
    create_wordcloud
)

# ==========================================================
# DASHBOARD KPI
# ==========================================================

def dashboard_kpi(df):

    kpi = {

        "Total Review": len(df),

        "Dominant Emotion": df["emotion"].mode()[0],

        "Dominant Segment": df["Customer Segment"].mode()[0],

        "Average Confidence": round(
            df["confidence"].mean()*100,
            2
        )

    }

    return kpi


# ==========================================================
# EMOTION SUMMARY
# ==========================================================

def emotion_summary(df):

    summary = (

        df

        .groupby("emotion")

        .size()

        .reset_index(name="Total")

        .sort_values(
            "Total",
            ascending=False
        )

    )

    return summary


# ==========================================================
# SEGMENT SUMMARY
# ==========================================================

def segment_summary(df):

    summary = (

        df

        .groupby("Customer Segment")

        .size()

        .reset_index(name="Total")

        .sort_values(
            "Total",
            ascending=False
        )

    )

    return summary


# ==========================================================
# PRIORITY SUMMARY
# ==========================================================

def priority_summary(df):

    summary = (

        df

        .groupby("Priority")

        .size()

        .reset_index(name="Total")

        .sort_values(
            "Total",
            ascending=False
        )

    )

    return summary


# ==========================================================
# DASHBOARD CHART
# ==========================================================

def dashboard_chart(df):

    chart = {

        "emotion_pie": emotion_pie(df),

        "emotion_bar": emotion_bar(df),

        "segment_bar": segment_bar(df),

        "segment_pie": segment_pie(df),

        "priority_bar": priority_bar(df),

        "confidence_histogram": confidence_histogram(df),

        "heatmap": probability_heatmap(df),

        "wordcloud": create_wordcloud(df)

    }

    return chart


# ==========================================================
# REVIEW STATISTICS
# ==========================================================

def review_statistics(df):

    review_length = (

        df["processed_text"]

        .astype(str)

        .apply(

            lambda x: len(x.split())

        )

    )

    return {

        "Average Review Length":

            round(review_length.mean(),2),

        "Maximum Review Length":

            review_length.max(),

        "Minimum Review Length":

            review_length.min()

    }


# ==========================================================
# DOWNLOAD DATASET
# ==========================================================

def download_dataset(df):

    return df.to_csv(

        index=False

    ).encode("utf-8-sig")


# ==========================================================
# TOP 10 WORD
# ==========================================================

def top_word(df):

    text = " ".join(

        df["processed_text"]

        .astype(str)

    )

    words = text.split()

    frequency = pd.Series(words)

    frequency = (

        frequency

        .value_counts()

        .head(10)

        .reset_index()

    )

    frequency.columns = [

        "Word",

        "Frequency"

    ]

    return frequency


# ==========================================================
# EMOTION PERCENTAGE
# ==========================================================

def emotion_percentage(df):

    percentage = (

        df["emotion"]

        .value_counts(

            normalize=True

        )

        *100

    ).round(2)

    percentage = percentage.reset_index()

    percentage.columns=[

        "Emotion",

        "Percentage"

    ]

    return percentage


# ==========================================================
# SEGMENT PERCENTAGE
# ==========================================================

def segment_percentage(df):

    percentage = (

        df["Customer Segment"]

        .value_counts(

            normalize=True

        )

        *100

    ).round(2)

    percentage = percentage.reset_index()

    percentage.columns=[

        "Customer Segment",

        "Percentage"

    ]

    return percentage


# ==========================================================
# DASHBOARD REPORT
# ==========================================================

def dashboard_report(df):

    report = {

        "KPI":

            dashboard_kpi(df),

        "Emotion":

            emotion_summary(df),

        "Segment":

            segment_summary(df),

        "Priority":

            priority_summary(df),

        "Statistics":

            review_statistics(df),

        "Top Word":

            top_word(df),

        "Emotion Percentage":

            emotion_percentage(df),

        "Segment Percentage":

            segment_percentage(df)

    }

    return report
