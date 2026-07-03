"""
=========================================================
DATA UNDERSTANDING
=========================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(

    page_title="Data Understanding",

    page_icon="📊",

    layout="wide"

)

st.title("📊 Data Understanding")

st.markdown("---")

# =====================================================
# CHECK DATASET
# =====================================================

if "raw_df" not in st.session_state:

    st.warning("Silakan upload dataset terlebih dahulu.")

    st.stop()

df = st.session_state["raw_df"]

# =====================================================
# DATASET OVERVIEW
# =====================================================

st.subheader("Dataset Overview")

col1,col2,col3,col4,col5 = st.columns(5)

with col1:

    st.metric(

        "Jumlah Review",

        len(df)

    )

with col2:

    st.metric(

        "Jumlah Kolom",

        len(df.columns)

    )

with col3:

    st.metric(

        "Missing Value",

        df.isnull().sum().sum()

    )

with col4:

    st.metric(

        "Duplicate",

        df.duplicated().sum()

    )

with col5:

    if "content" in df.columns:

        avg = round(

            df["content"]

            .astype(str)

            .apply(len)

            .mean(),

            2

        )

    else:

        avg = 0

    st.metric(

        "Avg Character",

        avg

    )

st.markdown("---")

# =====================================================
# PREVIEW
# =====================================================

st.subheader("Preview Dataset")

st.dataframe(

    df,

    use_container_width=True,

    height=400

)

# =====================================================
# COLUMN INFORMATION
# =====================================================

st.markdown("---")

st.subheader("Column Information")

info = pd.DataFrame({

    "Column":df.columns,

    "Data Type":df.dtypes.astype(str),

    "Missing":df.isnull().sum().values,

    "Unique":df.nunique().values

})

st.dataframe(

    info,

    use_container_width=True

)

# =====================================================
# MISSING VALUE
# =====================================================

st.markdown("---")

st.subheader("Missing Value Analysis")

missing = pd.DataFrame(

    df.isnull().sum(),

    columns=["Missing"]

)

missing = missing.reset_index()

missing.columns=[

    "Column",

    "Missing"

]

fig = px.bar(

    missing,

    x="Column",

    y="Missing",

    text_auto=True

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =====================================================
# DUPLICATE
# =====================================================

st.markdown("---")

st.subheader("Duplicate Data")

duplicate = df.duplicated().sum()

st.metric(

    "Duplicate Review",

    duplicate

)

# =====================================================
# DISTRIBUTION SCORE
# =====================================================

if "score" in df.columns:

    st.markdown("---")

    st.subheader("Rating Distribution")

    rating = (

        df["score"]

        .value_counts()

        .sort_index()

        .reset_index()

    )

    rating.columns=[

        "Rating",

        "Total"

    ]

    fig = px.bar(

        rating,

        x="Rating",

        y="Total",

        text_auto=True

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =====================================================
# REVIEW LENGTH
# =====================================================

if "content" in df.columns:

    st.markdown("---")

    st.subheader("Review Length")

    length = df.copy()

    length["Length"] = length["content"] \
        .astype(str) \
        .apply(lambda x: len(x.split()))

    fig = px.histogram(

        length,

        x="Length",

        nbins=30

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =====================================================
# WORD CLOUD
# =====================================================

if "content" in df.columns:

    st.markdown("---")

    st.subheader("WordCloud")

    text = " ".join(

        df["content"]

        .astype(str)

    )

    wc = WordCloud(

        width=1200,

        height=500,

        background_color="white"

    ).generate(text)

    fig,ax = plt.subplots(

        figsize=(14,6)

    )

    ax.imshow(

        wc,

        interpolation="bilinear"

    )

    ax.axis("off")

    st.pyplot(fig)

# =====================================================
# TOP WORD
# =====================================================

if "content" in df.columns:

    st.markdown("---")

    st.subheader("Top 20 Frequent Word")

    words = " ".join(

        df["content"]

        .astype(str)

    ).split()

    top = (

        pd.Series(words)

        .value_counts()

        .head(20)

        .reset_index()

    )

    top.columns=[

        "Word",

        "Frequency"

    ]

    fig = px.bar(

        top,

        x="Word",

        y="Frequency",

        text_auto=True

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =====================================================
# DATASET DESCRIPTION
# =====================================================

st.markdown("---")

st.subheader("Dataset Statistics")

st.dataframe(

    df.describe(

        include="all"

    ),

    use_container_width=True

)

# =====================================================
# SAVE SESSION
# =====================================================

st.session_state["understanding_df"] = df
