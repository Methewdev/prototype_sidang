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

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Upload Dataset")

st.markdown("---")

st.info(
"""
Silakan upload dataset hasil scraping Google Play.

Format yang didukung:

• CSV

• Excel (.xlsx)
"""
)

uploaded_file = st.file_uploader(

    "Upload Dataset",

    type=["csv","xlsx"]

)

if uploaded_file:

    with st.spinner("Membaca dataset..."):

        try:

            df = read_dataset(uploaded_file)

            save_session(

                "raw_df",

                df

            )

            st.success(

                "Dataset berhasil diupload."

            )

        except Exception as e:

            st.error(e)

            st.stop()

    # =====================================
    # KPI
    # =====================================

    info = dataset_info(df)

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(

        "Jumlah Review",

        info["rows"]

    )

    c2.metric(

        "Jumlah Kolom",

        info["columns"]

    )

    c3.metric(

        "Missing",

        info["missing"]

    )

    c4.metric(

        "Duplicate",

        info["duplicate"]

    )

    st.markdown("---")

    st.subheader("Preview Dataset")

    st.dataframe(

        df,

        use_container_width=True,

        height=450

    )

    st.markdown("---")

    st.subheader("Dataset Information")

    st.dataframe(

        dataframe_info(df),

        use_container_width=True

    )

    st.markdown("---")

    st.download_button(

        "⬇ Download Dataset",

        download_csv(df),

        "uploaded_dataset.csv",

        "text/csv"

    )

else:

    st.warning(

        "Silakan upload dataset terlebih dahulu."

    )
