"""
=========================================================
EMOTION PROBABILITY MODULE
=========================================================
Probability Visualization
=========================================================
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.prediction import predict_text
from config import EMOTION_LABELS

# ==========================================================
# SINGLE PROBABILITY
# ==========================================================

def probability_dataframe(text):

    emotion, confidence, probability = predict_text(text)

    df = pd.DataFrame({
        "Emotion": EMOTION_LABELS,
        "Probability": probability
    })

    return df


# ==========================================================
# BAR CHART
# ==========================================================

def probability_bar_chart(text):

    df = probability_dataframe(text)

    fig = px.bar(
        df,
        x="Emotion",
        y="Probability",
        color="Emotion",
        text_auto=".2f"
    )

    fig.update_layout(
        title="Emotion Probability",
        xaxis_title="Emotion",
        yaxis_title="Probability",
        height=450
    )

    return fig


# ==========================================================
# PIE CHART
# ==========================================================

def probability_pie_chart(text):

    df = probability_dataframe(text)

    fig = px.pie(
        df,
        values="Probability",
        names="Emotion",
        hole=0.4
    )

    fig.update_layout(
        title="Emotion Probability Distribution",
        height=450
    )

    return fig


# ==========================================================
# CONFIDENCE GAUGE
# ==========================================================

def confidence_gauge(text):

    emotion, confidence, probability = predict_text(text)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=confidence * 100,
            title={"text": "Confidence Score"},
            gauge={
                "axis": {"range": [0, 100]}
            }
        )
    )

    fig.update_layout(height=350)

    return fig


# ==========================================================
# TOP EMOTION
# ==========================================================

def top_emotion(text):

    emotion, confidence, probability = predict_text(text)

    return emotion


# ==========================================================
# TOP PROBABILITY
# ==========================================================

def top_probability(text):

    emotion, confidence, probability = predict_text(text)

    return round(confidence * 100, 2)


# ==========================================================
# PROBABILITY TABLE
# ==========================================================

def probability_table(text):

    df = probability_dataframe(text)

    df["Probability"] = (
        df["Probability"] * 100
    ).round(2)

    return df


# ==========================================================
# MULTIPLE REVIEW
# ==========================================================

def dataframe_probability(df):

    data = df.copy()

    data["Dominant Emotion"] = data[
        EMOTION_LABELS
    ].idxmax(axis=1)

    data["Confidence"] = data[
        EMOTION_LABELS
    ].max(axis=1)

    return data


# ==========================================================
# HEATMAP
# ==========================================================

def probability_heatmap(df):

    fig = px.imshow(
        df[EMOTION_LABELS].T,
        aspect="auto",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        title="Emotion Probability Heatmap",
        height=500
    )

    return fig


# ==========================================================
# AVERAGE PROBABILITY
# ==========================================================

def average_probability(df):

    avg = (
        df[EMOTION_LABELS]
        .mean()
        .reset_index()
    )

    avg.columns = [
        "Emotion",
        "Average Probability"
    ]

    return avg


# ==========================================================
# AVERAGE BAR CHART
# ==========================================================

def average_probability_chart(df):

    avg = average_probability(df)

    fig = px.bar(
        avg,
        x="Emotion",
        y="Average Probability",
        color="Emotion",
        text_auto=".2f"
    )

    fig.update_layout(
        title="Average Emotion Probability",
        height=450
    )

    return fig


# ==========================================================
# SUMMARY
# ==========================================================

def probability_summary(df):

    return {

        "Average Confidence":

        round(

            df["Confidence"].mean() * 100,

            2

        ),

        "Dominant Emotion":

        df["Dominant Emotion"].mode()[0]

    }
