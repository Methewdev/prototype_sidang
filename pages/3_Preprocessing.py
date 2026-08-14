"""
=========================================================
PREPROCESSING
=========================================================
Pipeline:

4.3.1 Cleaning
4.3.2 Case Folding
4.3.3 Normalization
4.3.4 Tokenization

Catatan:
- Stopword Removal tidak digunakan
- Stemming tidak digunakan
- Repeated Character Handling menjadi bagian dari Normalization
- Emoji dipertahankan sebagai sinyal emosional
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
**Pipeline yang digunakan dalam penelitian:**

1. **Cleaning**
2. **Case Folding**
3. **Normalization**
4. **Tokenization**

**Catatan:** Stopword Removal dan Stemming tidak digunakan karena penelitian menggunakan model Transformer/BERT yang mempertahankan konteks kata dalam kalimat.

Penanganan karakter berulang dilakukan sebagai bagian dari tahap **Normalization**, bukan sebagai tahap preprocessing tersendiri.
""")


st.markdown("---")


# =====================================================
# RUN PREPROCESSING
# =====================================================

if st.button(
    "🚀 Jalankan Preprocessing",
    use_container_width=True
):

    progress = st.progress(0)

    status = st.empty()


    # -------------------------------------------------
    # STEP 1
    # -------------------------------------------------

    status.info(
        "Tahap 1/4: Cleaning..."
    )

    progress.progress(25)


    # -------------------------------------------------
    # STEP 2
    # -------------------------------------------------

    status.info(
        "Tahap 2/4: Case Folding..."
    )

    progress.progress(50)


    # -------------------------------------------------
    # STEP 3
    # -------------------------------------------------

    status.info(
        "Tahap 3/4: Normalization..."
    )

    progress.progress(75)


    # -------------------------------------------------
    # RUN ACTUAL PREPROCESSING
    # -------------------------------------------------

    preprocess_df = preprocess_dataframe(
        df,
        text_column
    )


    # -------------------------------------------------
    # STEP 4
    # -------------------------------------------------

    status.info(
        "Tahap 4/4: Tokenization..."
    )

    progress.progress(100)


    # -------------------------------------------------
    # SAVE SESSION
    # -------------------------------------------------

    save_session(
        "preprocess_df",
        preprocess_df
    )


    status.success(
        "Preprocessing selesai."
    )


# =====================================================
# CHECK SESSION
# =====================================================

if "preprocess_df" not in st.session_state:

    st.info(
        "Klik tombol **Jalankan Preprocessing** untuk memproses dataset."
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
# PREPROCESSING RESULT
# =====================================================

st.subheader(
    "📋 Hasil Setiap Tahapan Preprocessing"
)


# =====================================================
# TABS
# =====================================================

tabs = st.tabs([

    "🧹 Cleaning",

    "🔡 Case Folding",

    "🔄 Normalization",

    "✂ Tokenization",

    "📄 Final Text"

])


# =====================================================
# PIPELINE DISPLAY
# =====================================================

pipeline = [

    # -------------------------------------------------
    # 4.3.1 Cleaning
    # -------------------------------------------------

    (
        text_column,
        "cleaning"
    ),

    # -------------------------------------------------
    # 4.3.2 Case Folding
    # -------------------------------------------------

    (
        "cleaning",
        "case_folding"
    ),

    # -------------------------------------------------
    # 4.3.3 Normalization
    # -------------------------------------------------

    (
        "case_folding",
        "normalization"
    ),

    # -------------------------------------------------
    # 4.3.4 Tokenization
    # -------------------------------------------------

    (
        "normalization",
        "token"
    ),

    # -------------------------------------------------
    # Final Text
    # -------------------------------------------------

    (
        "normalization",
        "final_text"
    )

]


# =====================================================
# DISPLAY RESULT
# =====================================================

for tab, (
    before,
    after
) in zip(
    tabs,
    pipeline
):

    with tab:

        # -------------------------------------------------
        # CHECK BEFORE COLUMN
        # -------------------------------------------------

        if before not in preprocess_df.columns:

            st.warning(
                f"Kolom '{before}' tidak ditemukan."
            )

            continue


        # -------------------------------------------------
        # CHECK AFTER COLUMN
        # -------------------------------------------------

        if after not in preprocess_df.columns:

            st.warning(
                f"Kolom '{after}' tidak ditemukan."
            )

            continue


        # -------------------------------------------------
        # PREVIEW
        # -------------------------------------------------

        preview = preprocess_df[
            [
                before,
                after
            ]
        ].copy()


        # -------------------------------------------------
        # TOKEN LIST -> STRING
        # -------------------------------------------------

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


        # -------------------------------------------------
        # DISPLAY
        # -------------------------------------------------

        st.dataframe(

            preview,

            use_container_width=True,

            height=450

        )


# =====================================================
# SUMMARY
# =====================================================

st.markdown("---")

st.subheader(
    "📌 Ringkasan Preprocessing"
)

st.markdown("""
Dataset telah melalui empat tahap preprocessing utama:

**Cleaning → Case Folding → Normalization → Tokenization**

Hasil akhir pada kolom **Final Text** digunakan sebagai input teks untuk proses selanjutnya, yaitu tokenisasi menggunakan tokenizer model Transformer dan proses klasifikasi emosi.
""")
