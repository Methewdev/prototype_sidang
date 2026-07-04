"""
=========================================================
PREPROCESSING
=========================================================
"""

import streamlit as st
import nltk

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")
    
from modules.utils import (
    require_session,
    save_session,
    download_csv,
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
    "raw_df",
    "Silakan upload dataset terlebih dahulu."
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

st.subheader("⚙ Preprocessing Pipeline")

st.markdown("""
- ✔ Cleaning
- ✔ Case Folding
- ✔ Clean Text
- ✔ Lexical Normalization
- ✔ Stopword Removal
- ✔ Stemming
- ✔ Tokenization
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

    status.info("Cleaning...")

    preprocess_df = preprocess_dataframe(
        df,
        text_column
    )

    progress.progress(100)

    status.success("Preprocessing selesai.")

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

preprocess_df = st.session_state["preprocess_df"]

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
    empty_review(preprocess_df)
)

c4.metric(
    "Average Length",
    average_length(preprocess_df)
)

st.markdown("---")

# =====================================================
# TABS
# =====================================================

st.subheader("📋 Hasil Setiap Tahapan Preprocessing")

tabs = st.tabs([
    "🧹 Cleaning",
    "🔡 Case Folding",
    "🔄 Normalization",
    "🚫 Stopword",
    "🌱 Stemming",
    "✂ Tokenization",
    "📄 Final Text"
])

# gunakan kolom asli apabila tersedia
original_col = text_column if text_column in preprocess_df.columns else "cleaning"

pipeline = [
    (original_col, "cleaning"),
    ("cleaning", "case_folding"),
    ("case_folding", "normalization"),
    ("normalization", "stopword"),
    ("stopword", "stemming"),
    ("stemming", "token"),
    ("stemming", "final_text")
]

for tab, (before, after) in zip(tabs, pipeline):

    with tab:

        if before not in preprocess_df.columns:
            st.warning(f"Kolom '{before}' tidak ditemukan.")
            continue

        if after not in preprocess_df.columns:
            st.warning(f"Kolom '{after}' tidak ditemukan.")
            continue

        # Hindari duplicate column
        cols = []
        for c in [before, after]:
            if c not in cols:
                cols.append(c)

        preview = preprocess_df[cols].copy()

        # token berupa list agar mudah dibaca
        if after == "token":
            preview["token"] = preview["token"].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )

        st.dataframe(
            preview,
            use_container_width=True,
            height=450
        )
