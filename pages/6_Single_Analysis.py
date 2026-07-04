"""
=========================================================
SINGLE REVIEW ANALYSIS
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.preprocessing import preprocess_single_review
from modules.prediction import predict_single_review

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Single Review Analysis",
    page_icon="📝",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("📝 Single Review Analysis")

st.caption(
    "Analisis emosi untuk satu review menggunakan Fine-Tuned IndoBERT."
)

st.divider()

# =====================================================
# INPUT
# =====================================================

review = st.text_area(

    "Masukkan Review",

    height=180,

    placeholder="Contoh:\nLivin sering logout sendiri ketika akan transfer."

)

analyze = st.button(

    "🚀 Analyze Review",

    use_container_width=True

)

# =====================================================
# ANALYSIS
# =====================================================

if analyze:

    if review.strip() == "":

        st.warning("Silakan masukkan review terlebih dahulu.")

        st.stop()

    # ==============================================
    # PREPROCESSING
    # ==============================================

    preprocess = preprocess_single_review(review)

    # ==============================================
    # PREDICTION
    # ==============================================

    prediction = predict_single_review(

        preprocess["final_text"]

    )

    st.success("Analisis berhasil dilakukan.")

    st.divider()

    # ==============================================
    # PREPROCESSING RESULT
    # ==============================================

    st.subheader("🧹 Preprocessing Result")

    preprocess_df = pd.DataFrame({

        "Step":[

            "Original",

            "Cleaning",

            "Case Folding",

            "Normalization",

            "Stopword Removal",

            "Stemming",

            "Final Text"

        ],

        "Result":[

            preprocess["original_text"],

            preprocess["cleaning"],

            preprocess["case_folding"],

            preprocess["normalization"],

            preprocess["stopword"],

            preprocess["stemming"],

            preprocess["final_text"]

        ]

    })

    st.dataframe(

        preprocess_df,

        width="stretch",

        hide_index=True

    )

    st.divider()

    # ==============================================
    # TOKENIZATION
    # ==============================================

    st.subheader("🔠 Tokenization")

    token_df = pd.DataFrame({

        "No":range(

            1,

            len(preprocess["token"])+1

        ),

        "Token":preprocess["token"]

    })

    st.dataframe(

        token_df,

        width="stretch",

        hide_index=True

    )

    st.divider()

    # ==============================================
    # PREDICTION RESULT
    # ==============================================

    st.subheader("🎯 Prediction Result")

    c1, c2 = st.columns(2)

    c1.metric(

        "Emotion",

        prediction["emotion"]

    )

    c2.metric(

        "Confidence",

        f"{prediction['confidence']*100:.2f}%"

    )

    st.divider()

    # ==============================================
    # PROBABILITY
    # ==============================================

    st.subheader("📈 Emotion Probability")

    probability = prediction["probability"]

    probability_df = pd.DataFrame({

        "Emotion":list(

            probability.keys()

        ),

        "Probability":[

            round(v*100,2)

            for v in probability.values()

        ]

    })

    st.bar_chart(

        probability_df.set_index(

            "Emotion"

        )

    )

    st.dataframe(

        probability_df,

        width="stretch",

        hide_index=True

    )
