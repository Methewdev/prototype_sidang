"""
=========================================================
PREPROCESSING
=========================================================
"""

import streamlit as st

from modules.utils import (
    require_session,
    save_session,
    detect_text_column
)

from modules.preprocessing import (
    preprocess_dataframe,
    preprocessing_statistics,
    empty_review,
    average_length
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Preprocessing",
    page_icon="🧹",
    layout="wide"
)


st.title("🧹 Text Preprocessing")

st.markdown("---")


# =====================================================
# LOAD DATASET
# =====================================================

df = require_session(
    "raw_data",
    "Silakan lakukan scraping terlebih dahulu pada menu Live Scraper."
)


text_column = detect_text_column(df)


if text_column is None:

    st.error(
        "Kolom review tidak ditemukan."
    )

    st.stop()


# =====================================================
# DATASET INFO
# =====================================================

c1, c2 = st.columns(2)


c1.metric(
    "Total Review",
    len(df)
)


c2.metric(
    "Text Column",
    text_column
)


st.markdown("---")


# =====================================================
# PIPELINE
# =====================================================

st.subheader(
    "⚙ Preprocessing Pipeline"
)


st.markdown("""
**Pipeline yang digunakan:**

1. Cleaning
2. Case Folding
3. Normalization
4. Repeated Character Handling
5. Tokenization

> Stopword Removal dan Stemming tidak digunakan karena penelitian menggunakan model Transformer/BERT yang mempertahankan konteks kata dalam kalimat.
""")


st.markdown("---")


# =====================================================
# RUN
# =====================================================

if st.button(
    "🚀 Jalankan Preprocessing",
    use_container_width=True
):

    progress = st.progress(0)

    status = st.empty()


    status.info(
        "Menjalankan preprocessing..."
    )


    progress.progress(10)


    preprocess_df = preprocess_dataframe(
        df,
        text_column
    )


    progress.progress(100)


    status.success(
        "Preprocessing selesai."
    )


    save_session(
        "preprocess_df",
        preprocess_df
    )


# =====================================================
# SESSION
# =====================================================

if "preprocess_df" not in st.session_state:

    st.info(
        "Klik tombol Jalankan Preprocessing."
    )

    st.stop()


preprocess_df = (
    st.session_state[
        "preprocess_df"
    ]
)


st.markdown("---")


# =====================================================
# STATISTICS
# =====================================================

stats = preprocessing_statistics(
    preprocess_df
)


c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Total Review",
    stats["Total Review"]
)


c2.metric(
    "Processed",
    stats["Cleaning"]
)


c3.metric(
    "Empty Review",
    empty_review(
        preprocess_df
    )
)


c4.metric(
    "Average Length",
    average_length(
        preprocess_df
    )
)


st.markdown("---")


# =====================================================
# TABS
# =====================================================

st.subheader(
    "📋 Hasil Setiap Tahapan Preprocessing"
)


tabs = st.tabs([

    "🧹 Cleaning",

    "🔡 Case Folding",

    "🔄 Normalization",

    "🔁 Repeated Character",

    "✂ Tokenization",

    "📄 Final Text"

])


# =====================================================
# PIPELINE DISPLAY
# =====================================================

pipeline = [

    (
        text_column,
        "cleaning"
    ),

    (
        "cleaning",
        "case_folding"
    ),

    (
        "case_folding",
        "normalization"
    ),

    (
        "normalization",
        "repeated_character"
    ),

    (
        "repeated_character",
        "token"
    ),

    (
        "repeated_character",
        "final_text"
    )

]


# =====================================================
# DISPLAY
# =====================================================

for tab, (
    before,
    after
) in zip(
    tabs,
    pipeline
):

    with tab:

        if before not in preprocess_df.columns:

            st.warning(
                f"Kolom '{before}' tidak ditemukan."
            )

            continue


        if after not in preprocess_df.columns:

            st.warning(
                f"Kolom '{after}' tidak ditemukan."
            )

            continue


        preview = preprocess_df[
            [
                before,
                after
            ]
        ].copy()


        # Token berupa list
        if after == "token":

            preview["token"] = (
                preview["token"]
                .apply(
                    lambda x:
                    ", ".join(x)
                    if isinstance(
                        x,
                        list
                    )
                    else x
                )
            )


        st.dataframe(

            preview,

            use_container_width=True,

            height=450

        )
