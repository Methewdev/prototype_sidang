"""
=========================================================
UPLOAD DATASET
=========================================================
"""

import streamlit as st
import pandas as pd

from config import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Upload Dataset")

st.markdown("---")

st.write(
"""
Silakan upload dataset hasil scraping Google Play
dalam format CSV atau Excel.
"""
)

# ==========================================================
# INITIAL SESSION
# ==========================================================

if "raw_df" not in st.session_state:
    st.session_state["raw_df"] = None

# ==========================================================
# FILE UPLOADER
# ==========================================================

uploaded_file = st.file_uploader(

    "Upload Dataset",

    type=["csv","xlsx"]

)

# ==========================================================
# LOAD FILE
# ==========================================================

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)

    st.session_state["raw_df"] = df

# ==========================================================
# DISPLAY DATA
# ==========================================================

if st.session_state["raw_df"] is not None:

    df = st.session_state["raw_df"]

    st.success("Dataset berhasil diupload")

    st.markdown("---")

    col1,col2,col3,col4 = st.columns(4)

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

    st.markdown("---")

    st.subheader("Preview Dataset")

    st.dataframe(

        df,

        use_container_width=True,

        height=500

    )

    st.markdown("---")

    st.subheader("Informasi Dataset")

    info = pd.DataFrame({

        "Column":df.columns,

        "Data Type":df.dtypes.astype(str),

        "Missing":df.isnull().sum().values

    })

    st.dataframe(

        info,

        use_container_width=True

    )

    st.markdown("---")

    st.download_button(

        "⬇ Download Dataset",

        data=df.to_csv(index=False),

        file_name="uploaded_dataset.csv",

        mime="text/csv"

    )

else:

    st.info("Silakan upload dataset terlebih dahulu.")
