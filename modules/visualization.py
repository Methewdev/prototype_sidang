"""
=========================================================
VISUALIZATION MODULE
=========================================================
"""

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from wordcloud import WordCloud

from config import EMOTION_LABELS
# =====================================================
# PIE CHART
# =====================================================

def emotion_pie(df):

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

        title="Emotion Distribution"

    )

    return fig
    # =====================================================
# BAR CHART
# =====================================================

def emotion_bar(df):

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

        color="Emotion",

        text_auto=True

    )

    fig.update_layout(

        height=400

    )

    return fig
    # =====================================================
# SEGMENT
# =====================================================

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

        color="Segment",

        text_auto=True

    )

    return fig
    # =====================================================
# PRIORITY
# =====================================================

def priority_bar(df):

    priority = (

        df["Priority"]

        .value_counts()

        .reset_index()

    )

    priority.columns = [

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

    return fig
    # =====================================================
# CONFIDENCE
# =====================================================

def confidence_histogram(df):

    fig = px.histogram(

        df,

        x="confidence",

        nbins=20

    )

    return fig
    # =====================================================
# HEATMAP
# =====================================================

def probability_heatmap(df):

    probability = df[EMOTION_LABELS]

    fig = px.imshow(

        probability.T,

        aspect="auto",

        labels={

            "x":"Review",

            "y":"Emotion",

            "color":"Probability"

        }

    )

    return fig
    # =====================================================
# WORD CLOUD
# =====================================================

def create_wordcloud(df):

    text = " ".join(

        df["final_text"]

        .astype(str)

    )

    wc = WordCloud(

        width=1200,

        height=600,

        background_color="white"

    ).generate(text)

    fig, ax = plt.subplots(

        figsize=(12,6)

    )

    ax.imshow(wc)

    ax.axis("off")

    return fig
    # =====================================================
# TOP WORD
# =====================================================

from collections import Counter

def top_words(

    df,

    n=20

):

    words = " ".join(

        df["final_text"]

    ).split()

    counter = Counter(words)

    data = pd.DataFrame(

        counter.most_common(n),

        columns=[

            "Word",

            "Frequency"

        ]

    )

    return data
    # =====================================================
# KPI
# =====================================================

def dashboard_kpi(df):

    return {

        "Total Review":len(df),

        "Emotion":

        df["emotion"].mode()[0],

        "Segment":

        df["Customer Segment"].mode()[0],

        "Confidence":

        round(

            df["confidence"].mean()*100,

            2

        )

    }
    
