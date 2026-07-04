import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

EMOTIONS = [
    "Frustrasi",
    "Netral",
    "Sedih",
    "Senang"
]


# =====================================================
# BUILD PROBABILITY DATAFRAME
# =====================================================

def dataframe_probability(df):

    result = df.copy()

    # jika model hanya menghasilkan confidence
    if "confidence" in result.columns:

        for emotion in EMOTIONS:

            if emotion not in result.columns:
                result[emotion] = 0.0

        if "emotion" in result.columns:

            for emotion in EMOTIONS:

                mask = result["emotion"] == emotion

                result.loc[mask, emotion] = result.loc[
                    mask,
                    "confidence"
                ]

    return result


# =====================================================
# SUMMARY
# =====================================================

def probability_summary(df):

    avg = round(
        df["confidence"].mean() * 100,
        2
    )

    dominant = (
        df["emotion"]
        .mode()
        .iloc[0]
    )

    return {

        "Average Confidence": avg,

        "Dominant Emotion": dominant

    }


# =====================================================
# AVERAGE
# =====================================================

def average_probability(df):

    avg = (

        df[EMOTIONS]

        .mean()

        .reset_index()

    )

    avg.columns = [

        "Emotion",

        "Probability"

    ]

    avg["Probability"] = (

        avg["Probability"] * 100

    ).round(2)

    return avg


# =====================================================
# BAR
# =====================================================

def average_probability_chart(df):

    avg = average_probability(df)

    fig = px.bar(

        avg,

        x="Emotion",

        y="Probability",

        text="Probability",

        color="Emotion"

    )

    fig.update_layout(

        height=450,

        title="Average Emotion Probability"

    )

    return fig


# =====================================================
# HEATMAP
# =====================================================

def probability_heatmap(df):

    if len(df) == 0:

        return go.Figure()

    fig = px.imshow(

        df[EMOTIONS],

        labels=dict(

            x="Emotion",

            y="Review",

            color="Probability"

        ),

        aspect="auto"

    )

    fig.update_layout(

        height=500,

        title="Emotion Probability Heatmap"

    )

    return fig
