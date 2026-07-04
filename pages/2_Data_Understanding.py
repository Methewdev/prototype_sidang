"""
=========================================================
DATA UNDERSTANDING
=========================================================
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from modules.utils import require_session

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Data Understanding",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Understanding")
st.caption("Eksplorasi dataset hasil scraping Google Play Store")

st.divider()

# =====================================================
# LOAD DATA
# =====================================================

df = require_session(
    "raw_data",
    "Silakan lakukan scraping terlebih dahulu pada menu Live Scraper."
)

# =====================================================
# METRICS
# =====================================================

latest = (
    df["date"].max().strftime("%d-%m-%Y")
    if "date" in df.columns and not df.empty
    else "-"
)

oldest = (
    df["date"].min().strftime("%d-%m-%Y")
    if "date" in df.columns and not df.empty
    else "-"
)

avg_rating = (
    round(df["rating"].mean(), 2)
    if "rating" in df.columns
    else 0
)

version = (
    df["app_version"].nunique()
    if "app_version" in df.columns
    else 0
)

reply = (
    df["developer_reply"].notna().sum()
    if "developer_reply" in df.columns
    else 0
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Review", len(df))
c2.metric("Average Rating", avg_rating)
c3.metric("Latest Review", latest)
c4.metric("Oldest Review", oldest)
c5.metric("App Version", version)

st.divider()

# =====================================================
# DATASET PREVIEW
# =====================================================

st.subheader("📄 Dataset Preview")

st.dataframe(
    df,
    width="stretch",
    hide_index=True,
    height=450
)

st.divider()

# =====================================================
# COLUMN INFORMATION
# =====================================================

st.subheader("📋 Column Information")

info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing": df.isnull().sum().values,
    "Unique": df.nunique().values
})

st.dataframe(
    info,
    width="stretch",
    hide_index=True
)

st.divider()

# =====================================================
# RATING DISTRIBUTION
# =====================================================

if "rating" in df.columns:

    st.subheader("⭐ Rating Distribution")

    rating = (
        df["rating"]
        .value_counts()
        .sort_index()
    )

    st.bar_chart(rating)

st.divider()

# =====================================================
# REVIEW TIMELINE
# =====================================================

if "date" in df.columns:

    st.subheader("📅 Review Timeline")

    timeline = (
        df.groupby(df["date"].dt.date)
        .size()
    )

    st.line_chart(timeline)

st.divider()

# =====================================================
# APP VERSION
# =====================================================

if "app_version" in df.columns:

    st.subheader("📱 App Version Distribution")

    version = (
        df["app_version"]
        .fillna("Unknown")
        .value_counts()
        .head(10)
    )

    st.bar_chart(version)

st.divider()

# =====================================================
# REVIEW LENGTH
# =====================================================

if "review" in df.columns:

    st.subheader("📏 Review Length Analysis")

    length = (
        df["review"]
        .fillna("")
        .astype(str)
        .str.split()
        .apply(len)
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Average", round(length.mean(), 2))
    c2.metric("Minimum", int(length.min()))
    c3.metric("Maximum", int(length.max()))

    fig, ax = plt.subplots(figsize=(8,4))

    ax.hist(length)

    ax.set_xlabel("Jumlah Kata")

    ax.set_ylabel("Jumlah Review")

    st.pyplot(fig)

st.divider()

# =====================================================
# MISSING VALUE
# =====================================================

st.subheader("❌ Missing Value")

missing = pd.DataFrame({

    "Column": df.columns,

    "Missing": df.isnull().sum().values,

    "Percentage": (

        df.isnull().sum()

        / len(df)

        *100

    ).round(2)

})

st.dataframe(
    missing,
    width="stretch",
    hide_index=True
)

st.divider()

# =====================================================
# DUPLICATE
# =====================================================

st.subheader("🔄 Duplicate Review")

duplicate = df.duplicated(subset="review").sum()

st.metric(
    "Duplicate Review",
    duplicate
)

st.divider()

# =====================================================
# DEVELOPER REPLY
# =====================================================

if "developer_reply" in df.columns:

    st.subheader("💬 Developer Reply")

    st.metric(
        "Total Reply",
        reply
    )

st.divider()

# =====================================================
# TOP HELPFUL REVIEW
# =====================================================

if "likes" in df.columns:

    st.subheader("👍 Top Helpful Reviews")

    top = (

        df

        .sort_values(

            "likes",

            ascending=False

        )

        .head(10)

    )

    st.dataframe(

        top[
            [
                "rating",
                "likes",
                "review"
            ]
        ],

        width="stretch",

        hide_index=True

    )

st.divider()

# =====================================================
# WORD CLOUD
# =====================================================

if "review" in df.columns:

    st.subheader("☁ Word Cloud")

    text = " ".join(

        df["review"]

        .fillna("")

        .astype(str)

    )

    wc = WordCloud(

        width=1200,

        height=600,

        background_color="white"

    ).generate(text)

    fig, ax = plt.subplots(figsize=(14,6))

    ax.imshow(wc)

    ax.axis("off")

    st.pyplot(fig)
