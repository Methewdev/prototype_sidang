"""
=========================================================
UPLOAD DATASET
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.utils import (
    save_session,
    download_csv
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Upload Dataset")

st.markdown("---")

# =====================================================
# UPLOAD FILE
# =====================================================

uploaded_file = st.file_uploader(
    "Upload Dataset (.csv atau .xlsx)",
    type=[
        "csv",
        "xlsx"
    ]
)

# =====================================================
# READ FILE
# =====================================================

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)

    save_session(
        "raw_df",
        df
    )

    st.success(
        "Dataset berhasil diupload."
    )

    st.markdown("---")

    # =================================================
    # METRIC
    # =================================================

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

    # =================================================
    # PREVIEW
    # =================================================

    st.subheader("Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )

    st.markdown("---")

    # =================================================
    # COLUMN INFORMATION
    # =================================================

    st.subheader("Column Information")

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

    # =================================================
    # DOWNLOAD
    # =================================================

    st.download_button(
        label="⬇ Download Dataset",
        data=download_csv(df),
        file_name="dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info(
        "Silakan upload dataset untuk memulai proses analisis."
    )
