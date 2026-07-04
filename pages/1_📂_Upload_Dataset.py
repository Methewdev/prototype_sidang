"""
=========================================================
UPLOAD DATASET
=========================================================
"""

import streamlit as st

from modules.utils import (
    read_dataset,
    save_session,
    dataset_info,
    dataframe_info,
    download_csv
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Upload Dataset")
st.markdown("---")

st.info("""
Silakan upload dataset hasil scraping Google Play.

**Format yang didukung:**
- CSV (.csv)
- Excel (.xlsx)
""")

# =====================================================
# FILE UPLOADER
# =====================================================

uploaded_file = st.file_uploader(
    "Pilih Dataset",
    type=["csv", "xlsx"]
)

# =====================================================
# LOAD DATASET
# =====================================================

if uploaded_file is not None:

    try:

        with st.spinner("Membaca dataset..."):

            df = read_dataset(uploaded_file)

            save_session("raw_df", df)

        st.success("Dataset berhasil diupload.")

    except Exception as e:

        st.error(e)

        st.stop()

    # Metric
    info = dataset_info(df)

    ...

else:

    st.warning("Silakan upload dataset.")

    # =====================================================
    # METRIC
    # =====================================================

    info = dataset_info(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📄 Jumlah Review",
        info["rows"]
    )

    c2.metric(
        "📑 Jumlah Kolom",
        info["columns"]
    )

    c3.metric(
        "❗ Missing Value",
        info["missing"]
    )

    c4.metric(
        "📌 Duplicate",
        info["duplicate"]
    )

    st.markdown("---")

    # =====================================================
    # PREVIEW DATASET
    # =====================================================

    st.subheader("📄 Preview Dataset")

    st.dataframe(
        df.head(20),
        use_container_width=True,
        height=450
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
    # DOWNLOAD
    # =====================================================

    st.download_button(
        "⬇ Download Dataset",
        data=download_csv(df),
        file_name="uploaded_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.warning("Silakan upload dataset terlebih dahulu.")
