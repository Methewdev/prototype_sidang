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

# =====================================================
# PAGE CONFIG
# =====================================================

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
# DATASET INFORMATION
# =====================================================

info = dataset_info(df)

c1, c2, c3, c4 = st.columns(4)

c1.metric("📄 Jumlah Review", info["rows"])
c2.metric("📑 Jumlah Kolom", info["columns"])
c3.metric("❗ Missing Value", info["missing"])
c4.metric("📌 Duplicate", info["duplicate"])

st.markdown("---")

# =====================================================
# PREVIEW DATASET
# =====================================================

st.subheader("📄 Preview Dataset")

st.dataframe(
    df.head(20),
    use_container_width=True,
    height=400
)

st.markdown("---")

# =====================================================
# DATAFRAME INFORMATION
# =====================================================

st.subheader("📋 Informasi Dataset")

st.dataframe(
    dataframe_info(df),
    use_container_width=True
)

# =====================================================
# STATISTIK NUMERIK
# =====================================================

numeric = df.select_dtypes(include=["number"])

if not numeric.empty:

    st.markdown("---")

    st.subheader("📈 Statistik Numerik")

    st.dataframe(
        numeric.describe().T,
        use_container_width=True
    )

# =====================================================
# DISTRIBUSI RATING
# =====================================================

rating_col = detect_rating_column(df)

if rating_col:

    st.markdown("---")

    st.subheader("⭐ Distribusi Rating")

    rating = (
        df[rating_col]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rating.columns = [
        "Rating",
        "Jumlah"
    ]

    fig = px.bar(
        rating,
        x="Rating",
        y="Jumlah",
        text="Jumlah",
        color="Rating"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# PANJANG REVIEW
# =====================================================

text_col = detect_text_column(df)

if text_col:

    st.markdown("---")

    st.subheader("📝 Distribusi Panjang Review")

    temp = df.copy()

    temp["Jumlah Kata"] = (

        temp[text_col]

        .fillna("")

        .astype(str)

        .str.split()

        .str.len()

    )

    fig = px.histogram(

        temp,

        x="Jumlah Kata",

        nbins=30

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =====================================================
# REVIEW PER TANGGAL
# =====================================================

date_col = detect_date_column(df)

if date_col:

    st.markdown("---")

    st.subheader("📅 Review per Tanggal")

    temp = df.copy()

    temp[date_col] = pd.to_datetime(

        temp[date_col],

        errors="coerce"

    )

    review = (

        temp

        .groupby(date_col)

        .size()

        .reset_index(name="Jumlah")

    )

    fig = px.line(

        review,

        x=date_col,

        y="Jumlah",

        markers=True

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =====================================================
# MISSING VALUE
# =====================================================

st.markdown("---")

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

left, right = st.columns([1,2])

with left:

    st.dataframe(

        missing,

        use_container_width=True

    )

with right:

    fig = px.bar(

        missing,

        x="Kolom",

        y="Missing",

        text="Missing",

        color="Missing"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =====================================================
# DUPLICATE
# =====================================================

st.markdown("---")

st.subheader("📌 Duplicate Data")

duplicate = int(df.duplicated().sum())

if duplicate > 0:

    st.warning(

        f"Ditemukan {duplicate} data duplikat."

    )

else:

    st.success(

        "Tidak ditemukan data duplikat."

    )

# =====================================================
# SAMPLE REVIEW
# =====================================================

if text_col:

    st.markdown("---")

    st.subheader("💬 Contoh Review")

    st.dataframe(

        df[[text_col]].head(10),

        use_container_width=True

    )
