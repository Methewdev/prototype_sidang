"""
=========================================================
DATA UNDERSTANDING
=========================================================
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud

from modules.utils import (
    require_session,
    detect_text_column
)

st.set_page_config(
    page_title="Data Understanding",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Understanding")

st.markdown("---")

# =====================================================
# LOAD DATASET
# =====================================================

df = require_session(
    "raw_df",
    "Silakan upload dataset terlebih dahulu."
)

text_column = detect_text_column(df)

# =====================================================
# METRIC
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Review",
    len(df)
)

c2.metric(
    "Total Column",
    len(df.columns)
)

c3.metric(
    "Missing Value",
    int(df.isnull().sum().sum())
)

c4.metric(
    "Duplicate",
    int(df.duplicated().sum())
)

st.markdown("---")

# =====================================================
# DATASET PREVIEW
# =====================================================

st.subheader("📄 Dataset Preview")

st.dataframe(
    df,
    use_container_width=True,
    height=450
)

st.markdown("---")

# =====================================================
# COLUMN INFORMATION
# =====================================================

st.subheader("📋 Column Information")

info = pd.DataFrame({

    "Column": df.columns,

    "Data Type": df.dtypes.astype(str),

    "Missing":

        df.isnull().sum().values,

    "Unique":

        df.nunique().values

})

st.dataframe(
    info,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# MISSING VALUE
# =====================================================

st.subheader("❌ Missing Value Analysis")

missing = pd.DataFrame({

    "Column": df.columns,

    "Missing":

        df.isnull().sum().values,

    "Percentage":

        (

            df.isnull().sum()

            / len(df)

            *100

        ).round(2)

})

st.dataframe(
    missing,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DUPLICATE
# =====================================================

st.subheader("🔄 Duplicate Analysis")

duplicate = df[df.duplicated()]

st.metric(
    "Duplicate Data",
    len(duplicate)
)

if len(duplicate):

    st.dataframe(
        duplicate,
        use_container_width=True
    )

else:

    st.success(
        "Tidak ditemukan data duplikat."
    )

st.markdown("---")

# =====================================================
# REVIEW LENGTH
# =====================================================

st.subheader("📏 Review Length Analysis")

if text_column:

    length = (

        df[text_column]

        .fillna("")

        .astype(str)

        .str.split()

        .apply(len)

    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average",
        round(length.mean(),2)
    )

    c2.metric(
        "Minimum",
        int(length.min())
    )

    c3.metric(
        "Maximum",
        int(length.max())
    )

    fig, ax = plt.subplots()

    ax.hist(length)

    ax.set_title("Review Length Distribution")

    st.pyplot(fig)

st.markdown("---")

# =====================================================
# RATING DISTRIBUTION
# =====================================================

if "score" in df.columns:

    st.subheader("⭐ Rating Distribution")

    rating = (

        df["score"]

        .value_counts()

        .sort_index()

    )

    st.bar_chart(rating)

    st.markdown("---")

# =====================================================
# WORD CLOUD
# =====================================================

if text_column:

    st.subheader("☁ Word Cloud")

    text = " ".join(

        df[text_column]

        .fillna("")

        .astype(str)

    )

    wc = WordCloud(

        width=1000,

        height=500,

        background_color="white"

    ).generate(text)

    fig, ax = plt.subplots(figsize=(14,6))

    ax.imshow(wc)

    ax.axis("off")

    st.pyplot(fig)
