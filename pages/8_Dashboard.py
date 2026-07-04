"""
=========================================================
DASHBOARD
=========================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from modules.utils import (
    require_session,
    download_csv
)

from modules.visualization import (
    emotion_bar,
    emotion_pie,
    confidence_histogram,
    segment_bar
)

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard")
st.markdown("---")

# =====================================================
# LOAD DATA
# =====================================================

retention_df = require_session(
    "retention_df",
    "Silakan lakukan seluruh proses analisis terlebih dahulu."
)

# =====================================================
# METRICS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Review",
    len(retention_df)
)

c2.metric(
    "Dominant Emotion",
    retention_df["emotion"].mode()[0]
    if "emotion" in retention_df.columns else "-"
)

c3.metric(
    "Dominant Segment",
    retention_df["Customer Segment"].mode()[0]
    if "Customer Segment" in retention_df.columns else "-"
)

c4.metric(
    "Average Confidence",
    f"{retention_df['confidence'].mean()*100:.2f}%"
    if "confidence" in retention_df.columns else "-"
)

st.markdown("---")

# =====================================================
# CHART
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("Emotion Distribution")

    st.plotly_chart(
        emotion_bar(retention_df),
        use_container_width=True
    )

with right:

    st.subheader("Emotion Pie")

    st.plotly_chart(
        emotion_pie(retention_df),
        use_container_width=True
    )

st.markdown("---")

left, right = st.columns(2)

with left:

    st.subheader("Customer Segment")

    st.plotly_chart(
        segment_bar(retention_df),
        use_container_width=True
    )

with right:

    st.subheader("Confidence Distribution")

    st.plotly_chart(
        confidence_histogram(retention_df),
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# RISK LEVEL
# =====================================================

if "Risk Level" in retention_df.columns:

    st.subheader("Risk Level")

    risk = (
        retention_df["Risk Level"]
        .value_counts()
        .reset_index()
    )

    risk.columns = [
        "Risk Level",
        "Total"
    ]

    st.dataframe(
        risk,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# CUSTOMER TYPE
# =====================================================

if "Customer Type" in retention_df.columns:

    st.subheader("Customer Type")

    customer = (
        retention_df["Customer Type"]
        .value_counts()
        .reset_index()
    )

    customer.columns = [
        "Customer Type",
        "Total"
    ]

    st.dataframe(
        customer,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# RETENTION STRATEGY
# =====================================================

if "Retention Strategy" in retention_df.columns:

    st.subheader("Retention Recommendation")

    cols = [
        c for c in [
            "Customer Type",
            "Risk Level",
            "Retention Strategy"
        ]
        if c in retention_df.columns
    ]

    st.dataframe(
        retention_df[cols].drop_duplicates(),
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# FINAL DATASET
# =====================================================

st.subheader("Final Dataset")

display_columns = [

    col for col in [

        "content",

        "emotion",

        "confidence",

        "Customer Segment",

        "Customer Type",

        "Risk Level",

        "Retention Strategy"

    ]

    if col in retention_df.columns

]

st.dataframe(
    retention_df[display_columns],
    use_container_width=True,
    height=500
)

st.markdown("---")

# =====================================================
# DOWNLOAD
# =====================================================

st.download_button(
    label="⬇ Download Final Result",
    data=download_csv(retention_df),
    file_name="dashboard_result.csv",
    mime="text/csv",
    use_container_width=True
)
