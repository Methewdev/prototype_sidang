"""
=========================================================
CLEANING PAGE
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.preprocessing import cleaning

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Cleaning",

    page_icon="🧹",

    layout="wide"

)

st.title("🧹 Text Cleaning")

st.markdown("---")

# ==========================================================
# CHECK DATA
# ==========================================================

if "raw_df" not in st.session_state:

    st.warning("Silakan upload dataset terlebih dahulu.")

    st.stop()

df = st.session_state["raw_df"].copy()

# ==========================================================
# TEXT COLUMN
# ==========================================================

possible_columns = [

    "content",

    "review",

    "ulasan"

]

text_column = None

for col in possible_columns:

    if col in df.columns:

        text_column = col

        break

if text_column is None:

    st.error("Kolom review tidak ditemukan.")

    st.stop()

# ==========================================================
# ORIGINAL DATA
# ==========================================================

st.subheader("Original Review")

st.dataframe(

    df[[text_column]].head(10),

    use_container_width=True

)

# ==========================================================
# PROCESS
# ==========================================================

with st.spinner("Cleaning text ..."):

    df["cleaning"] = df[text_column].apply(cleaning)

# ==========================================================
# RESULT
# ==========================================================

st.markdown("---")

st.subheader("Cleaning Result")

st.dataframe(

    df[

        [

            text_column,

            "cleaning"

        ]

    ].head(20),

    use_container_width=True

)

# ==========================================================
# COMPARISON
# ==========================================================

st.markdown("---")

st.subheader("Before vs After")

compare = pd.DataFrame({

    "Before":

        df[text_column].head(10),

    "After":

        df["cleaning"].head(10)

})

st.dataframe(

    compare,

    use_container_width=True

)

# ==========================================================
# STATISTICS
# ==========================================================

st.markdown("---")

st.subheader("Cleaning Statistics")

before_character = (

    df[text_column]

    .astype(str)

    .apply(len)

    .mean()

)

after_character = (

    df["cleaning"]

    .astype(str)

    .apply(len)

    .mean()

)

col1,col2,col3 = st.columns(3)

with col1:

    st.metric(

        "Total Review",

        len(df)

    )

with col2:

    st.metric(

        "Average Character (Before)",

        round(before_character,2)

    )

with col3:

    st.metric(

        "Average Character (After)",

        round(after_character,2)

    )

# ==========================================================
# DOWNLOAD
# ==========================================================

st.markdown("---")

st.download_button(

    "⬇ Download Cleaning Result",

    data=df.to_csv(index=False),

    file_name="cleaning_result.csv",

    mime="text/csv"

)

# ==========================================================
# SAVE SESSION
# ==========================================================

st.session_state["clean_df"] = df

st.success("Cleaning selesai.")
