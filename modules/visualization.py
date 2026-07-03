"""
=========================================================
VISUALIZATION MODULE
=========================================================
Plotly Visualization
=========================================================
"""

import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

import matplotlib.pyplot as plt

from config import EMOTION_COLOR

# ==========================================================
# EMOTION PIE CHART
# ==========================================================

def emotion_pie(df):

    emotion_count = (
        df["emotion"]
        .value_counts()
        .reset_index()
    )

    emotion_count.columns = [

        "Emotion",

        "Total"

    ]

    fig = px.pie(

        emotion_count,

        values="Total",

        names="Emotion",

        color="Emotion",

        color_discrete_map=EMOTION_COLOR,

        hole=0.4

    )

    fig.update_layout(

        title="Emotion Distribution",

        height=450

    )

    return fig


# ==========================================================
# EMOTION BAR
# ==========================================================

def emotion_bar(df):

    emotion_count = (
        df["emotion"]
        .value_counts()
        .reset_index()
    )

    emotion_count.columns = [

        "Emotion",

        "Total"

    ]

    fig = px.bar(

        emotion_count,

        x="Emotion",

        y="Total",

        color="Emotion",

        color_discrete_map=EMOTION_COLOR,

        text_auto=True

    )

    fig.update_layout(

        title="Emotion Distribution",

        height=450

    )

    return fig


# ==========================================================
# CONFIDENCE HISTOGRAM
# ==========================================================

def confidence_histogram(df):

    fig = px.histogram(

        df,

        x="confidence",

        nbins=20

    )

    fig.update_layout(

        title="Confidence Distribution",

        height=450

    )

    return fig


# ==========================================================
# SEGMENT BAR
# ==========================================================

def segment_bar(df):

    segment = (

        df["Customer Segment"]

        .value_counts()

        .reset_index()

    )

    segment.columns = [

        "Segment",

        "Total"

    ]

    fig = px.bar(

        segment,

        x="Segment",

        y="Total",

        text_auto=True

    )

    fig.update_layout(

        title="Customer Segment",

        height=450

    )

    return fig


# ==========================================================
# SEGMENT PIE
# ==========================================================

def segment_pie(df):

    segment = (

        df["Customer Segment"]

        .value_counts()

        .reset_index()

    )

    segment.columns=[

        "Segment",

        "Total"

    ]

    fig = px.pie(

        segment,

        values="Total",

        names="Segment",

        hole=0.4

    )

    fig.update_layout(

        title="Customer Segment Distribution",

        height=450

    )

    return fig


# ==========================================================
# PRIORITY BAR
# ==========================================================

def priority_bar(df):

    priority = (

        df["Priority"]

        .value_counts()

        .reset_index()

    )

    priority.columns=[

        "Priority",

        "Total"

    ]

    fig = px.bar(

        priority,

        x="Priority",

        y="Total",

        color="Priority",

        text_auto=True

    )

    fig.update_layout(

        title="Priority Distribution",

        height=450

    )

    return fig


# ==========================================================
# HEATMAP
# ==========================================================

def probability_heatmap(df):

    fig = px.imshow(

        df[

            [

                "Frustrasi",

                "Netral",

                "Sedih",

                "Senang"

            ]

        ].T,

        aspect="auto",

        color_continuous_scale="Blues"

    )

    fig.update_layout(

        title="Emotion Probability Heatmap",

        height=500

    )

    return fig


# ==========================================================
# WORD CLOUD
# ==========================================================

def create_wordcloud(df):

    text = " ".join(

        df["processed_text"]

        .astype(str)

    )

    wc = WordCloud(

        width=1000,

        height=500,

        background_color="white"

    ).generate(text)

    fig, ax = plt.subplots(

        figsize=(12,6)

    )

    ax.imshow(

        wc,

        interpolation="bilinear"

    )

    ax.axis("off")

    return fig


# ==========================================================
# KPI CARD
# ==========================================================

def dashboard_metric(df):

    return {

        "Total Review":len(df),

        "Dominant Emotion":

        df["emotion"].mode()[0],

        "Dominant Segment":

        df["Customer Segment"].mode()[0],

        "Average Confidence":

        round(

            df["confidence"].mean()*100,

            2

        )

    }


# ==========================================================
# EMOTION TABLE
# ==========================================================

def emotion_table(df):

    table = (

        df["emotion"]

        .value_counts()

        .reset_index()

    )

    table.columns=[

        "Emotion",

        "Total"

    ]

    return table


# ==========================================================
# SEGMENT TABLE
# ==========================================================

def segment_table(df):

    table=(

        df["Customer Segment"]

        .value_counts()

        .reset_index()

    )

    table.columns=[

        "Segment",

        "Total"

    ]

    return table


# ==========================================================
# PRIORITY TABLE
# ==========================================================

def priority_table(df):

    table=(

        df["Priority"]

        .value_counts()

        .reset_index()

    )

    table.columns=[

        "Priority",

        "Total"

    ]

    return table
