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
# FILE UPLOADER
# =====================================================

uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx"]
)

# =====================================================
# FUNCTION READ FILE
# =====================================================

def read_dataset(file):

    if file.name.lower().endswith(".xlsx"):
        return pd.read_excel(file)

    errors = []

    encodings = [
        "utf-8",
        "utf-8-sig",
        "latin1"
    ]

    separators = [
        ",",
        ";"
    ]

    for enc in encodings:

        for sep in separators:

            try:

                file.seek(0)

                df = pd.read_csv(
                    file,
                    encoding=enc,
                    sep=sep
                )

                if len(df.columns) > 1:
                    return df

            except Exception as e:
                errors.append(str(e))

    # Auto detect separator

    try:

        file.seek(0)

        return pd.read_csv(
            file,
            sep=None,
            engine="python"
        )

    except Exception as e:

        errors.append(str(e))

    raise Exception(
        "\n".join(errors)
    )

# =====================================================
# READ DATASET
# =====================================================

if uploaded_file is not None:

    try:

        df = read_dataset(uploaded_file)

    except Exception as e:

        st.error("❌ Dataset gagal dibaca.")

        st.exception(e)

        st.stop()

    # ===============================================

    save_session(
        "raw_df",
        df
    )

    st.success("✅ Dataset berhasil diupload.")

    st.markdown("---")

    # ===============================================
    # METRICS
    # ===============================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Jumlah Baris",
        f"{len(df):,}"
    )

    c2.metric(
        "Jumlah Kolom",
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

    # ===============================================
    # COLUMN LIST
    # ===============================================

    st.subheader("📋 Daftar Kolom")

    st.write(list(df.columns))

    st.markdown("---")

    # ===============================================
    # PREVIEW
    # ===============================================

    st.subheader("📄 Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True,
        height=450
    )

    st.markdown("---")

    # ===============================================
    # INFORMATION
    # ===============================================

    st.subheader("📊 Informasi Dataset")

    info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing": df.isnull().sum().values,
        "Unique": df.nunique().values
    })

    st.dataframe(
        info,
        use_container_width=True
    )

    st.markdown("---")

    # ===============================================
    # DOWNLOAD
    # ===============================================

    st.download_button(
        label="⬇ Download Dataset",
        data=download_csv(df),
        file_name="dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info(
        "Silakan upload dataset (.csv atau .xlsx) untuk memulai analisis."
    )
