"""
=========================================================
EMOTION PROBABILITY
=========================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from modules.visualization import (
    probability_heatmap,
    confidence_histogram
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Emotion Probability",

    page_icon="📈",

    layout="wide"

)

st.title("📈 Emotion Probability")

st.markdown("---")

# =====================================================
# CHECK SESSION
# =====================================================

if "prediction_df" not in st.session_state:

    st.warning(

        "Silakan lakukan Emotion Prediction terlebih dahulu."

    )

    st.stop()

df = st.session_state["prediction_df"]

# =====================================================
# KPI
# =====================================================

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(

        "Total Review",

        len(df)

    )

with col2:

    st.metric(

        "Average Confidence",

        f"{df['confidence'].mean()*100:.2f}%"

    )

with col3:

    st.metric(

        "Dominant Emotion",

        df["emotion"].mode()[0]

    )

with col4:

    st.metric(

        "Emotion Class",

        df["emotion"].nunique()

    )

st.markdown("---")

# =====================================================
# REVIEW SELECTOR
# =====================================================

st.subheader("Review Probability")

index = st.slider(

    "Pilih Review",

    0,

    len(df)-1,

    0

)

review = df.iloc[index]

st.info(review["normalization"])

# =====================================================
# PROBABILITY TABLE
# =====================================================

probability = pd.DataFrame({

    "Emotion":[

        "Frustrasi",

        "Netral",

        "Sedih",

        "Senang"

    ],

    "Probability":[

        review["Frustrasi"],

        review["Netral"],

        review["Sedih"],

        review["Senang"]

    ]

})

col1,col2 = st.columns(2)

with col1:

    st.dataframe(

        probability,

        use_container_width=True

    )

with col2:

    fig = px.bar(

        probability,

        x="Emotion",

        y="Probability",

        color="Emotion",

        text_auto=".2f"

    )

    fig.update_layout(

        height=350

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.markdown("---")

# =====================================================
# CONFIDENCE
# =====================================================

st.subheader("Confidence Distribution")

st.plotly_chart(

    confidence_histogram(df),

    use_container_width=True

)

# =====================================================
# HEATMAP
# =====================================================

st.markdown("---")

st.subheader("Emotion Probability Heatmap")

st.plotly_chart(

    probability_heatmap(df),

    use_container_width=True

)

# =====================================================
# SUMMARY
# =====================================================

st.markdown("---")

st.subheader("Average Probability")

summary = pd.DataFrame({

    "Emotion":[

        "Frustrasi",

        "Netral",

        "Sedih",

        "Senang"

    ],

    "Average":[

        df["Frustrasi"].mean(),

        df["Netral"].mean(),

        df["Sedih"].mean(),

        df["Senang"].mean()

    ]

})

fig = px.bar(

    summary,

    x="Emotion",

    y="Average",

    color="Emotion",

    text_auto=".2f"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =====================================================
# DOWNLOAD
# =====================================================

st.markdown("---")

st.download_button(

    "⬇ Download Probability",

    df.to_csv(index=False),

    "probability_result.csv",

    "text/csv"

)

# =====================================================
# SAVE SESSION
# =====================================================

st.session_state["probability_df"] = df

st.success(

    "Emotion Probability selesai."

)
