"""
=========================================================
PREPROCESSING
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.utils import (
    require_session,
    save_session,
    download_csv,
    detect_text_column
)

from modules.preprocessing import (
    preprocess_dataframe
)

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

    st.error("Kolom review tidak ditemukan.")

    st.stop()

# =====================================================
# RUN PREPROCESS
# =====================================================

if st.button(
    "🚀 Jalankan Preprocessing",
    use_container_width=True
):

    with st.spinner("Sedang melakukan preprocessing..."):

        preprocess_df = preprocess_dataframe(
            df,
            text_column=text_column
        )

        save_session(
            "preprocess_df",
            preprocess_df
        )

    st.success("Preprocessing selesai.")

# =====================================================
# DISPLAY
# =====================================================

if "preprocess_df" not in st.session_state:

    st.info(
        "Klik tombol **Jalankan Preprocessing**."
    )

    st.stop()

preprocess_df = st.session_state["preprocess_df"]

st.markdown("---")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(

    [

        "🧹 Cleaning",

        "🔡 Case Folding",

        "🔄 Normalization",

        "🚫 Stopword",

        "🌱 Stemming",

        "✂️ Tokenization"

    ]

)
with tab1:

    st.subheader("Cleaning")

    st.dataframe(

        preprocess_df[

            [

                text_column,

                "cleaning"

            ]

        ],

        use_container_width=True

    )
    with tab2:

    st.subheader("Case Folding")

    st.dataframe(

        preprocess_df[

            [

                "cleaning",

                "case_folding"

            ]

        ],

        use_container_width=True

    )
    with tab3:

    st.subheader("Normalization")

    st.dataframe(

        preprocess_df[

            [

                "case_folding",

                "normalization"

            ]

        ],

        use_container_width=True

    )
    with tab4:

    st.subheader("Stopword Removal")

    st.dataframe(

        preprocess_df[

            [

                "normalization",

                "stopword"

            ]

        ],

        use_container_width=True

    )
   with tab5:

    st.subheader("Stemming")

    st.dataframe(

        preprocess_df[

            [

                "stopword",

                "stemming"

            ]

        ],

        use_container_width=True

    )
       with tab5:

    st.subheader("Stemming")

    st.dataframe(

        preprocess_df[

            [

                "stopword",

                "stemming"

            ]

        ],

        use_container_width=True

    )
