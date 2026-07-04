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

display_columns = [
    col
    for col in [
        "prediction_id",
        "content",
        "clean_text",
        "final_text",
        "emotion",
        "confidence"
    ]
    if col in prediction_df.columns
]

st.subheader("Prediction Result")
st.dataframe(
    prediction_display[display_columns],
    use_container_width=True,
    hide_index=True
)
st.dataframe(
    prediction_df[
        display_columns
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
        emotion_bar(
            prediction_df
        ),
        use_container_width=True
    )

with right:

    st.plotly_chart(
        emotion_pie(
            prediction_df
        ),
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# CONFIDENCE
# =====================================================

st.subheader("Confidence Distribution")

st.plotly_chart(
    confidence_histogram(
        prediction_df
    ),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DOWNLOAD
# =====================================================

st.download_button(
    label="⬇ Download Prediction Result",
    data=download_csv(
        prediction_df
    ),
    file_name="prediction.csv",
    mime="text/csv",
    use_container_width=True
)
