"""
=========================================================
EMOTION PROBABILITY
=========================================================
"""

import streamlit as st

from modules.emotion_probability import (
    probability_table,
    probability_bar_chart,
    probability_pie_chart,
    confidence_gauge,
    top_emotion,
    top_probability
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion Probability",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Emotion Probability")

st.markdown("---")

# =====================================================
# INPUT TEXT
# =====================================================

text = st.text_area(
    "Masukkan kalimat yang ingin diprediksi",
    height=180,
    placeholder="Contoh: Aplikasi Livin sangat membantu transaksi saya."
)

# =====================================================
# BUTTON
# =====================================================

if st.button(
    "🚀 Predict Emotion",
    use_container_width=True
):

    if text.strip() == "":

        st.warning(
            "Silakan masukkan teks terlebih dahulu."
        )

        st.stop()

    # =================================================
    # METRIC
    # =================================================

    col1, col2 = st.columns(2)

    col1.metric(
        "Predicted Emotion",
        top_emotion(text)
    )

    col2.metric(
        "Confidence",
        f"{top_probability(text)} %"
    )

    st.markdown("---")

    # =================================================
    # TABLE
    # =================================================

    st.subheader("Probability Table")

    st.dataframe(
        probability_table(text),
        use_container_width=True
    )

    st.markdown("---")

    # =================================================
    # CHART
    # =================================================

    left, right = st.columns(2)

    with left:

        st.plotly_chart(
            probability_bar_chart(text),
            use_container_width=True
        )

    with right:

        st.plotly_chart(
            probability_pie_chart(text),
            use_container_width=True
        )

    st.markdown("---")

    # =================================================
    # GAUGE
    # =================================================

    st.subheader("Confidence Score")

    st.plotly_chart(
        confidence_gauge(text),
        use_container_width=True
    )
