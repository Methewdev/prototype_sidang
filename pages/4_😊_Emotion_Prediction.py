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
# RUN PREDICTION
# =====================================================

if st.button(
    "🚀 Jalankan Emotion Prediction",
    use_container_width=True
):

    with st.spinner("Model sedang melakukan prediksi..."):

        prediction_df = predict_dataframe(
            df,
            text_column="final_text"
        )

        save_session(
            "prediction_df",
            prediction_df
        )

    st.success("Prediction selesai.")

# =====================================================
# CHECK SESSION
# =====================================================

if "prediction_df" not in st.session_state:

    st.info(
        "Klik tombol **Jalankan Emotion Prediction**."
    )

    st.stop()

prediction_df = st.session_state["prediction_df"]

# =====================================================
# SUMMARY
# =====================================================

summary = prediction_summary(
    prediction_df
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Review",
    summary["Total Review"]
)

col2.metric(
    "Dominant Emotion",
    summary["Dominant Emotion"]
)

col3.metric(
    "Average Confidence",
    f"{summary['Average Confidence']} %"
)

st.markdown("---")

# =====================================================
# RESULT TABLE
# =====================================================

st.subheader("Prediction Result")

st.dataframe(
    prediction_df[
        [
            "content",
            "emotion",
            "confidence"
        ]
    ],
    use_container_width=True,
    height=450
)

st.markdown("---")

# =====================================================
# VISUALIZATION
# =====================================================

left, right = st.columns(2)

with left:

    st.plotly_chart(
        emotion_bar(prediction_df),
        use_container_width=True
    )

with right:

    st.plotly_chart(
        emotion_pie(prediction_df),
        use_container_width=True
    )

st.markdown("---")

st.subheader("Confidence Distribution")

st.plotly_chart(
    confidence_histogram(
        prediction_df
    ),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# EMOTION DISTRIBUTION
# =====================================================

st.subheader("Emotion Distribution")

emotion_table = (
    prediction_df["emotion"]
    .value_counts()
    .reset_index()
)

emotion_table.columns = [
    "Emotion",
    "Total"
]

emotion_table["Percentage"] = (
    emotion_table["Total"]
    /
    emotion_table["Total"].sum()
    * 100
).round(2)

st.dataframe(
    emotion_table,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DOWNLOAD
# =====================================================

st.download_button(
    label="⬇ Download Prediction Result",
    data=download_csv(prediction_df),
    file_name="prediction.csv",
    mime="text/csv",
    use_container_width=True
)
