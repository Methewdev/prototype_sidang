"""
=========================================================
DATA UNDERSTANDING
=========================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from modules.utils import (
    require_session,
    dataset_info,
    dataframe_info,
    detect_text_column,
    detect_rating_column,
    detect_date_column
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

# =====================================================
# DATASET INFO
# =====================================================

info = dataset_info(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Jumlah Review", info["rows"])
col2.metric("Jumlah Kolom", info["columns"])
col3.metric("Missing Value", info["missing"])
col4.metric("Duplicate Data", info["duplicate"])

st.markdown("---")

# =====================================================
# PREVIEW DATASET
# =====================================================

st.subheader("📄 Preview Dataset")

st.dataframe(
    df,
    use_container_width=True,
    height=350
)

st.markdown("---")

# =====================================================
# INFORMASI DATASET
# =====================================================

st.subheader("📋 Informasi Dataset")

st.dataframe(
    dataframe_info(df),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DISTRIBUSI RATING
# =====================================================

rating_col = detect_rating_column(df)

if rating_col:

    st.subheader("⭐ Distribusi Rating")

    rating = (
        df[rating_col]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rating.columns = ["Rating","Jumlah"]

    fig = px.bar(
        rating,
        x="Rating",
        y="Jumlah",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# PANJANG ULASAN
# =====================================================

text_col = detect_text_column(df)

if text_col:

    st.subheader("📝 Distribusi Panjang Ulasan")

    temp = df.copy()

    temp["Panjang Ulasan"] = (
        temp[text_col]
        .astype(str)
        .str.split()
        .str.len()
    )

    fig = px.histogram(
        temp,
        x="Panjang Ulasan",
        nbins=30
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# REVIEW PER TANGGAL
# =====================================================

date_col = detect_date_column(df)

if date_col:

    st.subheader("📅 Jumlah Review per Tanggal")

    temp = df.copy()

    temp[date_col] = pd.to_datetime(
        temp[date_col],
        errors="coerce"
    )

    review_date = (
        temp.groupby(date_col)
        .size()
        .reset_index(name="Jumlah Review")
    )

    fig = px.line(
        review_date,
        x=date_col,
        y="Jumlah Review",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# MISSING VALUE
# =====================================================

st.subheader("❗ Missing Value")

missing = (
    df.isnull()
      .sum()
      .reset_index()
)

missing.columns = [
    "Kolom",
    "Missing"
]

st.dataframe(
    missing,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DUPLICATE
# =====================================================

st.subheader("📌 Duplicate Data")

duplicate = df.duplicated().sum()

st.metric(
    "Jumlah Duplicate",
    duplicate
)

if duplicate > 0:

    st.warning(
        "Dataset masih memiliki data duplikat."
    )

else:

    st.success(
        "Tidak ditemukan data duplikat."
    )
