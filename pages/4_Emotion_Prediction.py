"""
=========================================================
EMOTION PREDICTION
=========================================================
"""

import streamlit as st

from modules.utils import (
    require_session,
    save_session,
    download_csv
)

from modules.prediction import (
    predict_dataframe,
    prediction_summary
)

from modules.visualization import (
    emotion_bar,
    emotion_pie,
    confidence_histogram
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion Prediction",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Emotion Prediction")

st.markdown("---")

# =====================================================
# LOAD PREPROCESSING RESULT
# =====================================================

df = require_session(
    "preprocess_df",
    "Silakan lakukan preprocessing terlebih dahulu."
)

# =====================================================
# DATASET INFO
# =====================================================

st.metric(
    "Total Review",
    len(df)
)

st.markdown("---")

# =====================================================
# RUN PREDICTION
# =====================================================

if st.button(
    "🚀 Jalankan Emotion Prediction",
    use_container_width=True
):

    progress = st.progress(0)

    status = st.empty()

    status.info("Model sedang melakukan prediksi...")

    prediction_df = predict_dataframe(
        df,
        text_column="final_text"
    )

    progress.progress(100)

    status.success("Prediction selesai.")

    save_session(
        "prediction_df",
        prediction_df
    )

# =====================================================
# CHECK SESSION
# =====================================================

if "prediction_df" not in st.session_state:

    st.info(
        "Klik tombol **Jalankan Emotion Prediction**."
    )

    st.stop()

prediction_df = st.session_state["prediction_df"]

st.markdown("---")

# =====================================================
# SUMMARY
# =====================================================

summary = prediction_summary(
    prediction_df
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Review",
    summary["Total Review"]
)

c2.metric(
    "Dominant Emotion",
    summary["Dominant Emotion"]
)

c3.metric(
    "Average Confidence",
    f"{summary['Average Confidence']} %"
)

st.markdown("---")

# =====================================================
# RESULT
# =====================================================

prediction_display = prediction_df.copy()

prediction_display["confidence"] = (
    prediction_display["confidence"] * 100
).round(2).astype(str) + " %"

display_columns = [
    col
    for col in [
        "prediction_id",
        "content",
        "final_text",
        "emotion",
        "confidence"
    ]
    if col in prediction_display.columns
]

# =====================================================
# VISUALIZATION
# =====================================================
st.subheader("Prediction Result")

st.dataframe(
    prediction_display[display_columns],
    use_container_width=True,
    hide_index=True,
    height=450
)

st.markdown("---")

# =====================================================
# VIEW REVIEW
# =====================================================

st.subheader("👁 View Review")

selected = st.selectbox(
    "Pilih Review",
    prediction_display["prediction_id"]
)

row = prediction_df[
    prediction_df["prediction_id"] == selected
].iloc[0]

st.markdown("### 📝 Original Review")
st.info(row["content"])

st.markdown("### 🧹 Final Text")
st.code(row["final_text"])

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Emotion",
        row["emotion"]
    )

with c2:
    st.metric(
        "Confidence",
        f"{row['confidence'] * 100:.2f}%"
    )

st.markdown("---")

# =====================================================
# VISUALIZATION
# =====================================================
