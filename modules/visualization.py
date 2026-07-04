import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from modules.visualization import (
    segment_bar
)
# =====================================================
# MISSING VALUE
# =====================================================

def missing_value_chart(df):

    missing = pd.DataFrame({

        "Column": df.columns,

        "Missing":

            df.isnull().sum().values

    })

    fig = px.bar(

        missing,

        x="Column",

        y="Missing",

        text="Missing",

        color="Missing"

    )

    fig.update_layout(

        title="Missing Value Distribution",

        xaxis_title="Column",

        yaxis_title="Total Missing",

        height=450

    )

    return fig
  # =====================================================
# RATING DISTRIBUTION
# =====================================================

def rating_distribution_chart(df):

    rating = (

        df["score"]

        .value_counts()

        .sort_index()

        .reset_index()

    )

    rating.columns = [

        "Rating",

        "Total"

    ]

    fig = px.bar(

        rating,

        x="Rating",

        y="Total",

        text="Total",

        color="Rating"

    )

    fig.update_layout(

        title="Rating Distribution",

        height=450

    )

    return fig
  # =====================================================
# REVIEW LENGTH
# =====================================================

def review_length_chart(df, text_column):

    data = df.copy()

    data["Review Length"] = (

        data[text_column]

        .fillna("")

        .astype(str)

        .str.split()

        .apply(len)

    )

    fig = px.histogram(

        data,

        x="Review Length",

        nbins=40

    )

    fig.update_layout(

        title="Review Length Distribution",

        height=450

    )

    return fig
  # =====================================================
# DUPLICATE
# =====================================================

def duplicate_chart(df):

    duplicate = int(df.duplicated().sum())

    unique = len(df) - duplicate

    fig = px.pie(

        names=[

            "Unique",

            "Duplicate"

        ],

        values=[

            unique,

            duplicate

        ],

        hole=0.45

    )

    fig.update_layout(

        title="Duplicate Distribution",

        height=450
        
    )

    return fig
    
# =====================================================
# EMOTION DISTRIBUTION
# =====================================================

def emotion_distribution_chart(df, emotion_column="emotion"):

    if emotion_column not in df.columns:
        return go.Figure()

    emotion = (
        df[emotion_column]
        .value_counts()
        .reset_index()
    )

    emotion.columns = ["Emotion", "Total"]

    fig = px.bar(
        emotion,
        x="Emotion",
        y="Total",
        text="Total",
        color="Emotion"
    )

    fig.update_layout(
        title="Emotion Distribution",
        height=450
    )

    return fig
    # =====================================================
# EMOTION PIE
# =====================================================

def emotion_pie_chart(df, emotion_column="emotion"):

    if emotion_column not in df.columns:
        return go.Figure()

    emotion = (
        df[emotion_column]
        .value_counts()
        .reset_index()
    )

    emotion.columns = ["Emotion", "Total"]

    fig = px.pie(
        emotion,
        names="Emotion",
        values="Total",
        hole=0.45
    )

    fig.update_layout(
        title="Emotion Distribution",
        height=450
    )

    return fig
    # =====================================================
# PROBABILITY
# =====================================================

def probability_chart(probability):

    if isinstance(probability, dict):

        prob = pd.DataFrame({

            "Emotion": probability.keys(),

            "Probability": probability.values()

        })

    else:

        prob = probability

    fig = px.bar(

        prob,

        x="Emotion",

        y="Probability",

        color="Emotion",

        text="Probability"

    )

    fig.update_layout(

        title="Emotion Probability",

        yaxis_range=[0,1],

        height=400

    )

    return fig
    # =====================================================
# CONFIDENCE
# =====================================================

def confidence_gauge(score):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score*100,

            title={"text":"Confidence"},

            gauge={

                "axis":{"range":[0,100]}

            }

        )

    )

    fig.update_layout(

        height=350

    )

    return fig
    # =====================================================
# WORD FREQUENCY
# =====================================================

def top_word_chart(df):

    if "Word" not in df.columns:

        return go.Figure()

    fig = px.bar(

        df,

        x="Frequency",

        y="Word",

        orientation="h"

    )

    fig.update_layout(

        title="Top Words",

        height=500

    )

    return fig
# =====================================================
# EMOTION BAR
# =====================================================

def emotion_bar(df):

    if "emotion" not in df.columns:
        return go.Figure()

    emotion = (
        df["emotion"]
        .value_counts()
        .reset_index()
    )

    emotion.columns = [
        "Emotion",
        "Total"
    ]

    fig = px.bar(
        emotion,
        x="Emotion",
        y="Total",
        text="Total",
        color="Emotion"
    )

    fig.update_layout(
        title="Emotion Distribution",
        height=450
    )

    return fig
    # =====================================================
# EMOTION PIE
# =====================================================

def emotion_pie(df):

    if "emotion" not in df.columns:
        return go.Figure()

    emotion = (
        df["emotion"]
        .value_counts()
        .reset_index()
    )

    emotion.columns = [
        "Emotion",
        "Total"
    ]

    fig = px.pie(
        emotion,
        names="Emotion",
        values="Total",
        hole=0.45
    )

    fig.update_layout(
        title="Emotion Distribution",
        height=450
    )

    return fig
    # =====================================================
# CONFIDENCE HISTOGRAM
# =====================================================

def confidence_histogram(df):

    if "confidence" not in df.columns:
        return go.Figure()

    fig = px.histogram(
        df,
        x="confidence",
        nbins=20
    )

    fig.update_layout(
        title="Confidence Distribution",
        xaxis_title="Confidence",
        yaxis_title="Total Review",
        height=450
    )

    return fig
    # =====================================================
# CUSTOMER SEGMENT BAR
# =====================================================

def segment_bar(df):

    if "Customer Segment" not in df.columns:
        return go.Figure()

    segment = (
        df["Customer Segment"]
        .value_counts()
        .reset_index()
    )

    segment.columns = [
        "Customer Segment",
        "Total"
    ]

    fig = px.bar(
        segment,
        x="Customer Segment",
        y="Total",
        text="Total",
        color="Customer Segment"
    )

    fig.update_layout(
        title="Customer Segment Distribution",
        height=450
    )

    return fig
